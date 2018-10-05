#!/usr/bin/perl
use warnings;
use DBI;
my $userid = "root";
my $password = "655321";

my $dbh = DBI->connect('DBI:mysql:usersDB;host=localhost', $userid, $password ) or die "This isn't working!";
my $sql = "INSERT INTO users(FIRST_NAME,LAST_NAME,DEPT,LEVEL) VALUES(?,?,?,?)";
my $stmt = $dbh->prepare($sql);
$stmt->execute('Larry','Gonyea','System Analyst',1);
#$dbh->do("INSERT INTO users ('first name','last name','department','role') VALUES (?,?,?,?)", undef, 'Larry','Gonyea','System Analyst','1');
$dbh->disconnect();

#DBD::mysql module