use strict;
use warnings;
my $total = 0;

my ($thisWeek, $checkedIn, $dow) = @ARGV;

sub thisWeek{
  if (not defined $thisWeek){
    print "This Week time: ";
    $thisWeek = <STDIN>;
  } else {
    thisWeek();
  }
}

sub checkedIn{
  if (not defined $checkedIn){
    print "Check In time: ";
    $checkedIn = <STDIN>;
  } else {
    checkedIn();
  }
}

if (not defined $thisWeek) {thisWeek();}
if (not defined $checkedIn) {checkedIn();}


$checkedIn =~ /(\d+)(.\d+)/;
$checkedIn = $1+($2*100/60);

if (not defined $dow) {
  $thisWeek = 40 - $thisWeek;
  $thisWeek =~ /(\d+)(.\d+)/;
  while ($thisWeek > 8){
    $thisWeek -= 8;
    my $total = $thisWeek + $checkedIn;
  }
} else {
  my $dowHours = (8 * $dow);
  $total = $dowHours - $thisWeek + $checkedIn;
}

$total =~ /(\d+)(.\d+)/;
$total = $1 + ($2 * .60);
if ($total > 12) {
  $total -= 12;
}

printf "Leave at: %2.2f\n", $total;
