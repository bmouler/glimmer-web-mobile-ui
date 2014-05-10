#!/usr/bin/perl -w

use strict;
use CGI;
use HTML::Template;
use DBI;

my $cgi = new CGI;
my $template = HTML::Template->new(filename => '/var/www/bmouler/final/tmpl/save_history.tmpl');
my $filename = $cgi->param("filename");
my $search_id = $cgi->param("search_id");


############################################################
##########Save Glimmer results to MySQL database
############################################################

my $dsn = 'DBI:mysql:database=bmouler;host=localhost';
my $opts = { RaiseError => 1, PrintError => 1 };
my $dbh = DBI->connect($dsn, 'bmouler', '4rmonattygy6', $opts);
$dbh->do("LOAD DATA LOCAL INFILE '/var/www/bmouler/final/uploads/$filename.txt' REPLACE INTO TABLE glimmer_history");
$dbh->disconnect();

############################################################


############################################################
##########Push results to HTML template
############################################################

$template->param(SEARCHID => "$search_id");

print $cgi -> header('text/html');
print $template->output;

############################################################