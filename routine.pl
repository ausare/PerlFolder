
#!usr/bin/perl
use strict;
use warnings;

my @snapshot = ingest();
my $blank = "";
my @cleanedSnap = cleanData(@snapshot);

my @individualArrayItems = @cleanedSnap[5,6];
output("output.txt", @cleanedSnap);

print @cleanedSnap;
#print @snapshot;
#print "This is the fourth line of snapshot $snapshot[4]";

my $inc = 0;
foreach (@cleanedSnap){
  $inc ++;
  print "$inc: $_";
}

sub ingest{
  open FH, '<', "snapshot9.txt";
  return <FH>;
  close FH;
}

sub cleanData{
  my @batchArray;
  foreach(@_){
    s/(?:\s{3,6})(\d{1,4})(?:\s{2})/\nEntry Number Is: $1\n/;
  }
  #   foreach(@_){
  #       s/..<.*\n//;
  #       s/..\///;
  #       if(/?<BatchType>(^Generic|^Batch|^Logical).*(?:queue\s)?<Queue>(\w+).*\n/){
  #	   $_ = "$+{BatchType} | $+{Queue}";
  #       }
  #   }

  ##open dir and read dir##

  output("array.txt",@batchArray);
  my $stringConvert = join "|",@_;
  output("stringConvert.txt",$stringConvert);

  #This works
  #
  #    if($stringConvert =~ /(Generic|Batch|Logical).*(?:queue\s)(\w+).*\n/g){
  #	push @batchArray, "$1 | $2";
  #    }
  #
  #    $stringConvert =~ s/^\|\s{2}Entry.*Username.*\n\|\s{2}\.*\n//g;
  #    $stringConvert =~ s/\s+/ /g;
  #    $stringConvert =~ /(::)?\n&//gm;
  #    $stringConvert =~ s/|\s{2}\///g;
  #    $stringConvert =~ s/<.*>\n//g;
  #
  #    $stringConvert =~ s/(\|)\n\1(\s{2})Entry\2Jobname.*\n\1\2----.*/\|/g;
  #    $stringConvert =~ s/(::)?\n\|\s{2}\<<?\w+.*>//g;
  #    $stringConvert =~ s/(::)?\n\|\s{2}\//\//g;
  #    $stringConvert =~ s/\n\| {3,9}//g;

  output("stringConvert2.txt",$stringConvert);
  #Next section: anything with an entry number will have the seperator removed
  #(so it stays in the same scalar as the queue).
  #    $stringConvert =~ s/^\| {3,}(\d{3,4}) {2}(\w+)\n/$1 $2/g;
  #    $stringConvert =~ s/^\|(?:\n| {3})(?:\/)(\w+)/$1/g;
  #    $stringConvert =~ s/^



  output("joined.txt", $stringConvert);

  @_ = split /\|/,$stringConvert;
  foreach(@_){
    #$_ =~ s/^\n$//;
  }
  <STDIN>;
  print "This is the first part of the split array: $_[0]";
  return @_;

}
output("output.txt", @cleanedSnap);

sub output{
  my ($fileName, @data) = @_;
  open FH,'>',"$fileName" or die "$fileName couldn't be created for output";
  print FH @data;
  close FH;
}
