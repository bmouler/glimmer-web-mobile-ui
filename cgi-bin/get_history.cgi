#!/usr/bin/perl -w

use strict;
use CGI;
use HTML::Template;
use DBI;

#Predeclared variables:
my $cgi = new CGI;
my $tmpl = HTML::Template -> new(filename => '/var/www/bmouler/final/tmpl/history.tmpl');
my $query = "%".$cgi->param('search_id')."%";
my @orf;
my @start;
my @finish;
my @length;
my @weight;
my @countA;
my @countC;
my @countG;
my @countT;
my @GCcontent;
my @sequence;
my @table;


############################################################
##########Query MySQL database
############################################################

my $dsn = 'DBI:mysql:database=bmouler;host=localhost';
my $dbh = DBI->connect($dsn, "bmouler", "4rmonattygy6", { RaiseError => 1, PrintError => 1 });

my $querySQL = qq{
    SELECT orf, start, finish, length, weight, countA, countC, countG, countT, GCcontent, sequence
    FROM glimmer_history
    WHERE id LIKE ?;
};

my $dsh = $dbh->prepare($querySQL);
$dsh->execute($query);

## iterate through the results
while ( my $row = $dsh->fetchrow_hashref ) {
    push @orf, "$$row{orf}";
    push @start, $$row{start};
    push @finish, $$row{finish};
    push @length, $$row{length};
    push @weight, $$row{weight};
    push @countA, $$row{countA};
    push @countC, $$row{countC};
    push @countG, $$row{countG};
    push @countT, $$row{countT};
    push @GCcontent, $$row{GCcontent};
    push @sequence, $$row{sequence};
}

## clean up
$dsh->finish();
$dbh->disconnect();

############################################################


############################################################
##########Push results to HTML template
############################################################

#Create data structure for table in HTML template
while (@orf and @start and @finish and @length and @sequence and @weight and @countA and @countC and @countG and @countT and @GCcontent) {
    my %rows;

    $rows{ORF} = shift @orf;
    $rows{START} = shift @start;
    $rows{FINISH} = shift @finish;
    $rows{LENGTH} = shift @length;
    $rows{SEQUENCE} = shift @sequence;
    $rows{WEIGHT} = shift @weight;
    $rows{COUNTA} = shift @countA;
    $rows{COUNTC} = shift @countC;
    $rows{COUNTG} = shift @countG;
    $rows{COUNTT} = shift @countT;
    $rows{GCCONTENT} = shift @GCcontent;
    
    push(@table, \%rows);
}
$tmpl -> param(TABLE => \@table );

print $cgi -> header('text/html');
print $tmpl -> output;

############################################################