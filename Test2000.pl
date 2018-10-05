
#!usr/bin/perl
use strict;
use warnings;

my $stringer = "|   4678  \n|967  ";

$stringer =~ s/\d{4}//;

print $stringer;
