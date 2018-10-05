#!/usr/bin/perl
while (<>) {                   # take one input line at a time
	chomp;
	if (/(?<word>\b\w*a\b)\s(.{0,5})/) {
		print "Matched: \'word\' contains \'$+{word}\' and \'$2\'\n";  # the special match vars
	} else {
		print "No match: |$_|\n";
	}
}
