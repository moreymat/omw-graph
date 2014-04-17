#!/usr/bin/perl
# -*- perl -*-
#
# Create the Kyoto-LMF version
#
# Copyright 2009 Francis Bond, NICT
#
# FIXME base-concept
#
use strict;
use warnings;
use DBI;
use utf8;
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

my $db = $ARGV[0]  || die "No database specified\n";
my $v =  $ARGV[1]  || die "No version specified\n";
my $lang =  $ARGV[2]  || die "No language specified\n";
my $label =  $ARGV[3]  || die "No label specified\n";
my $url =  $ARGV[4]  || "";
my $lic =  $ARGV[5]  || "";
my $owner = $ARGV[6]  || "";

my $dbh = DBI->connect("dbi:SQLite:dbname=$db", "", "", {AutoCommit => 0});
$dbh->{sqlite_unicode} = 1;

my %syns;

sub nm {
    my $text = $_[0];
    $text =~ s/"/XXX/g;
    $text =~ s/'/&apos;/g;
    $text =~ s/&/&amp;/g;
    $text =~ s/</&lt;/g;
    $text =~ s/>/&gt;/g;
    return $text
}

print STDERR "load Definitions\n";
my %defs;
my $stname = $dbh->prepare(
	"select synset, sid, def from synset_def where lang=? order by sid");
$stname->execute($lang);
while (my @row = $stname->fetchrow_array()) {
    $defs{$row[0]}[$row[1]] = &nm($row[2]);
}
print STDERR "load Examples\n";
my %exs;
$stname = $dbh->prepare(
	"select synset, sid, def from synset_ex where lang=? order by sid");
$stname->execute($lang);
while (my @row = $stname->fetchrow_array()) {
    $exs{$row[0]}[$row[1]] = &nm($row[2]);
}

print STDERR "load links\n";
my %links;
$stname = $dbh->prepare(
    "select synset1, link, synset2 from synlink");	
$stname->execute();
while (my @row = $stname->fetchrow_array()) {
    $links{$row[0]}{$row[1]}{$row[2]}++;
    $syns{$row[0]}++;
    $syns{$row[2]}++;
}
print STDERR "load senses\n";
my %senses_synset;
my %senses_word;
$stname = $dbh->prepare(
    "select synset, wordid from sense where lang=? order by lexid");	
$stname->execute($lang);
while (my @row = $stname->fetchrow_array()) {
    $senses_synset{$row[0]}{$row[1]}++;
    $senses_word{$row[1]}{$row[0]}++;
    $syns{$row[0]}++;
}
print STDERR "load words\n";
my %words;
$stname = $dbh->prepare(
    "select wordid, lemma, pos from word where lang=?");	
$stname->execute($lang);
while (my @row = $stname->fetchrow_array()) {
    $words{$row[0]}{"lemma"} = &nm($row[1]);
#    $words{$row[0]}{"lemma"} =~ s/<.*>//g;
    $words{$row[0]}{"pos"} = $row[2];
}


chop(my $date = `date --rfc-3339=date`);
print <<HEAD;
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE LexicalResource SYSTEM "WN-LMF.dtd">
<LexicalResource>
	<GlobalInformation label="${lang} WordNet ${v}"/>
        <!-- produced on ${date} -->
        <!-- as part of the Open Multilingual Wordnet http://compling.hss.ntu.edu.sg -->
        <!-- source at ${url} (may have a better version) -->
HEAD
    if ($lic) {
print "        <!-- licence: ${lic} -->\n"
}

    &printLexicon;
    &printSenseAxes;
    
print "</LexicalResource>\n";

sub printLexicon () {
    #my %rels = &getRelations;
    ### Header
    if ($owner) {
	print "<Lexicon languageCoding='ISO 639-3' label='$label' language='${lang}' owner='$owner' version='${v}'>\n";
    } else {
	print "<Lexicon languageCoding='ISO 639-3' label='$label' language='${lang}' version='${v}'>\n";
    }
    ### Lexical entries
    for my $wid (keys %words) {
	print "   <LexicalEntry id ='w$wid'>\n";
	print "      <Lemma writtenForm='", $words{$wid}{"lemma"};
	print "' partOfSpeech='".$words{$wid}{"pos"}."'/>\n";
	### Synsets
	for my $synset (keys  %{$senses_word{$wid}}) {
	    print "      <Sense id='w${wid	}_${synset}' synset='${lang}-${v}-$synset'/>\n";
	}
	print "   </LexicalEntry>\n";
    }
    #for my $synset (keys  %senses_synset) {
    for my $synset (keys  %links) {
        ## Synset identifier 
	print "   <Synset id='${lang}-${v}-$synset' baseConcept='3'>\n";
	## Definitions
	if ($defs{$synset}) {
	    my $def = join ";", @{$defs{$synset}};
	    if ($def) {
		print "      <Definition gloss=\"$def\">\n";
		for my $ex (@{$exs{$synset}}) {
		    print "         <Statement example=\"$ex\"/>\n";
		}
		print "      </Definition>\n";
	    }
	}
# 	<Definition gloss="天然生成的環境與事物。">
# 	    <Statement example="風景畫家走出工作室，開始描繪戶外的自然。"/>
# 	    </Definition>


	## Add links

        print "      <SynsetRelations>\n";
	for my $link (keys %{$links{$synset}}) {
	    for my $target (keys %{$links{$synset}{$link}}) {
		#my $rel = $rels{$link};
		my $rel=$link;
		print "         <SynsetRelation targets='${lang}-${v}-$target' relType='$rel'/>\n";
	    }
	}
        print "      </SynsetRelations>\n";
	## Add Sumo links


	### ugly but for some reason required
# 	print "   <MonolingualExternalRefs>\n";
# 	print "      <MonolingualExternalRef externalSystem='SUMO' externalReference='' relType='at'/>\n";
# 	print "      </MonolingualExternalRefs>\n";
	print "   </Synset>\n";
    }
    ### unlinked things
    for my $synset  (keys  %syns) {
	unless ( $links{$synset}) {
	    print STDERR "Orphan $synset\n";
	print "   <Synset id='${lang}-${v}-$synset' baseConcept='3'>\n";
        print "      <SynsetRelations>\n";
	### self link so we can validate
	    print "         <SynsetRelation targets='${lang}-${v}-$synset' relType='self'>";
	    print "</SynsetRelation>\n";
        print "      </SynsetRelations>\n";

	### ugly but for some reason required
	print "   <MonolingualExternalRefs>\n";
	print "      <MonolingualExternalRef externalSystem='' externalReference='' relType='at'/>\n";
	print "      </MonolingualExternalRefs>\n";
	print "   </Synset>\n";
	}
    }
    print "</Lexicon>\n";
}
sub printSenseAxes () {
    ### Header
    print "<SenseAxes>\n";
    my $sa_id =0;
    ### Equivalents
    #for my $synset (keys %senses_synset) {
    for my $synset (keys %links) {
	print "   <SenseAxis id='sa_${lang}-${v}-$sa_id' relType='eq_synonym'>\n";
	print "      <Target ID='${lang}-${v}-$synset'/>\n";
	print "      <Target ID='eng-30-$synset'/>\n";
	print "   </SenseAxis>\n";
	$sa_id++;
    }
    ### Footer
    print "</SenseAxes>\n";
}
$dbh->disconnect()  or warn "Disconnection failed: $DBI::errstr\n";

# sub getRelations () {
#     my %rels;
#     $rels{"also"} = "see also";  #?
#     $rels{"attr"} = "attribute"; #?
#     $rels{"caus"} = "is_caused_by";
#     $rels{"dmnc"} = "";
#     $rels{"dmnr"} = "";
#     $rels{"dmnu"} = "";
#     $rels{"dmtc"} = "";
#     $rels{"dmtr"} = "";
#     $rels{"dmtu"} = "";
#     $rels{"enta"} = "";
#     $rels{"hasi"} = "";
#     $rels{"hmem"} = "";
#     $rels{"hprt"} = "";
#     $rels{"hsub"} = "";
#     $rels{"hype"} = "";
#     $rels{"hypo"} = "";
#     $rels{"inst"} = "";
#     $rels{"mmem"} = "";
#     $rels{"mprt"} = "";
#     $rels{"msub"} = "";
#     $rels{"sim"} = "";
#     return %rels;
# }
