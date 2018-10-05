#! /usr/bin/perl
use strict;
use warnings;
use File::Find;

my $dir = ".";
my $locateFile = "/^rcop.*/";

find(\&wanted, $dir);

# my $found = `find $dir -type f -iname $locateFile`;

# print $found if $found;

my @oldNames;
sub wanted {
    if($_ =~ /^rcop/ && !-d){

   push(@oldNames, $File::Find::name);
#  print $File::Find::name . "\n";
#  print if -f;
    }

foreach(@oldNames){
    print $_ . "\n";
}
        
}

