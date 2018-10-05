#!/usr/bin/perl

use Net::FTP;
use warnings;
use File::Copy;

my @args = @ARGV;
my $destinationFolder = "/PerlTemp/";
my $photo = $args[0];
if ($photo =~ m/bin$/) {
$photo = substr($photo,0,-4);
}
downloadFile("ftp1.tmsgf.trb", "features", "0feats2", "pc", "$destinationFolder$photo", "$photo");
## Unstuffs downloaded file. Option "-e no" says to never put file in a folder. Leaving out this option will let 
##		stuffit to determine on it's own whether or not to do that. 
##		This became a problem because it was putting single photos in a folder. 
if ($photo =~ m/sit$/) {
system("/usr/bin/unstuff -e no $destinationFolder$photo >> /dev/null");
system("/bin/rm $destinationFolder$photo >> /dev/null");
}




sub downloadFile
{
	my @parameters = @_;
	my $server = "$parameters[0]";
	my $user = "$parameters[1]";
	my $pass = "$parameters[2]";
	my $init = "$parameters[3]";	#supports only one level
	my $path = "$parameters[4]";
	my $downloadname = "$parameters[5]";

	my $ftp = Net::FTP->new("$server", Debug => 0, Passive => 0);
	$ftp->login("$user","$pass");
	$ftp->binary();
	$ftp->cwd("$init");
	$ftp->get("$downloadname","$path") or warn (print "**WARNING** - Cannot find $photo on Features FTP\n");
	$ftp->quit;
	return 1;
}