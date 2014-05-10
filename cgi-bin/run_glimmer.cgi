#!/usr/bin/perl -w

use strict;
use CGI;
use HTML::Template;
use Bio::Tools::SeqStats;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

my $cgi = new CGI;
my $template = HTML::Template->new(filename => '/var/www/bmouler/final/tmpl/results.tmpl');

my $ref_file;
my $query_file;

$CGI::POST_MAX = 1024 * 100000; #Limit upload size to 100Mb
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir = "/var/www/bmouler/final/uploads/";


############################################################
##########Upload query sequence      
############################################################

$query_file = $cgi->param("query_seq");

if ( !$query_file ) {
    print $cgi->header ( );
    print "There was a problem uploading your file (size limit is 100Mb).";
    exit;
}

my ( $name, $path, $extension ) = fileparse ( $query_file, '\..*' );
$query_file = $name;
$query_file =~ tr/ /_/;
$query_file =~ s/[^$safe_filename_characters]//g;

if ( $query_file =~ /^([$safe_filename_characters]+)$/ ) {
$query_file = $1;
}
else {
    die "Filename contains invalid characters.";
}

my $upload_filehandle1 = $cgi->upload("query_seq");

open ( UPLOADFILE1, ">$upload_dir/QRY_$query_file.fasta" ) or die "$!";
binmode UPLOADFILE1;
$query_file = "QRY_$query_file";
while ( <$upload_filehandle1> ) {
    print UPLOADFILE1;
}

close UPLOADFILE1;

############################################################


############################################################
##########Upload reference sequence       
############################################################

$ref_file = $cgi->param("reference_seq");

if ($ref_file eq "") {
    $ref_file = $query_file;
}
else {
    if ( !$ref_file ) {
        print $cgi->header ( );
        print "There was a problem uploading your file (size limit is 100Mb).";
        exit;
    }

    ( $name, $path, $extension ) = fileparse ( $ref_file, '\..*' );
    $ref_file = $name;
    $ref_file =~ tr/ /_/;
    $ref_file =~ s/[^$safe_filename_characters]//g;
    
    if ( $ref_file =~ /^([$safe_filename_characters]+)$/ ) {
    $ref_file = $1;
    }
    else {
        die "Filename contains invalid characters.";
    }
    
    my $upload_filehandle2 = $cgi->upload("reference_seq");
    
    open ( UPLOADFILE2, ">$upload_dir/REF_$ref_file" ) or die "$!";
    binmode UPLOADFILE2;
    $ref_file = "REF_$ref_file.fasta";
    while ( <$upload_filehandle2> ) {
        print UPLOADFILE2;
    }
    
    close UPLOADFILE2;
}

############################################################


############################################################
##########long-orfs         
############################################################

my $long_orfs_cmd = "long-orfs -n";

my $long_orfs_o1 = $cgi->param("long_orfs_o1");
    $long_orfs_o1 = lc $long_orfs_o1;
    if ($long_orfs_o1 =~ m/([atcg]{3})\s*\,*\s*([atcg]{3})*\s*\,*\s*([atcg]{3})*/) {
        my $codon_list = $1;
        if (defined $2) {
            $codon_list .= ",$2";
            if (defined $3) {
                $codon_list .= ",$3";
            }
        }
        $long_orfs_cmd .= " -A $codon_list";
    }
        
my $long_orfs_o2 = $cgi->param("long_orfs_o2");
    if ($long_orfs_o2 =~ m/(d+)/) {
        $long_orfs_cmd .= " -g $1";
    }

my $long_orfs_o3 = $cgi->param("long_orfs_o3");
    if ($long_orfs_o3 =~ m/(d+)/) {
        $long_orfs_cmd .= " -o $1";
    }
    
my $long_orfs_o4 = $cgi->param("long_orfs_o4");
    if ($long_orfs_o4 =~ m/(d+)/) {
        $long_orfs_cmd .= " -t $1";
    }
    else {
        $long_orfs_cmd .= " -t 1.15";
    }
    
my $long_orfs_o5 = $cgi->param("long_orfs_o5");
    if ($long_orfs_o5 =~ m/(d+)/) {
        $long_orfs_cmd .= " -z $1";
    }
    
my $long_orfs_o6 = $cgi->param("long_orfs_o6");
$long_orfs_o6 = lc $long_orfs_o6;
    if ($long_orfs_o6 =~ m/([atcg]{3})\s*\,*\s*([atcg]{3})*\s*\,*\s*([atcg]{3})*/) {
        my $codon_list = $1;
        if (defined $2) {
            $codon_list .= ",$2";
            if (defined $3) {
                $codon_list .= ",$3";
            }
        }
        $long_orfs_cmd .= " -Z $codon_list";
    }
    
my $long_orfs_s1 = $cgi->param("long_orfs_s1");
    if ($long_orfs_s1 eq "1") {
        $long_orfs_cmd .= " -f";
    }
    
my $long_orfs_s2 = $cgi->param("long_orfs_s2");
    if ($long_orfs_s2 eq "1") {
        $long_orfs_cmd .= " -l";
    }
    
my $long_orfs_s3 = $cgi->param("long_orfs_s3");
    if ($long_orfs_s3 eq "1") {
        $long_orfs_cmd .= " -L";
    }

$long_orfs_cmd .= " $ref_file.fasta $ref_file.longorfs";

############################################################


############################################################
##########build-icm
############################################################

my $build_icm_cmd = "build-icm";


my $build_icm_o1 = $cgi->param("build_icm_o1");
    if ($build_icm_o1 =~ m/(d+)/) {
        $build_icm_cmd .= " -d $1";
    }
    
my $build_icm_o2 = $cgi->param("build_icm_o2");
    if ($build_icm_o2 =~ m/(d+)/) {
        $build_icm_cmd .= " -p $1";
    }
    
my $build_icm_o3 = $cgi->param("build_icm_o3");
    if ($build_icm_o3 =~ m/(d+)/) {
        $build_icm_cmd .= " -w $1";
    }
    
my $build_icm_o4 = $cgi->param("build_icm_o4");
    if ($build_icm_o4 =~ m/(d+)/) {
        $build_icm_cmd .= " -z $1";
    }
    
my $build_icm_o5 = $cgi->param("build_icm_o5");
    $build_icm_o5 = lc $build_icm_o5;
    if ($build_icm_o5 =~ m/([atcg]{3})\s*\,*\s*([atcg]{3})*\s*\,*\s*([atcg]{3})*/) {
        my $codon_list = $1;
        if (defined $2) {
            $codon_list .= ",$2";
            if (defined $3) {
                $codon_list .= ",$3";
            }
        }
        $build_icm_cmd .= " -Z $codon_list";
    }
    
my $build_icm_s1 = $cgi->param("build_icm_s1");
    if ($build_icm_s1 eq "1") {
        $build_icm_cmd .= " -F";
    }
    
my $build_icm_s2 = $cgi->param("build_icm_s2");
    if ($build_icm_s2 eq "1") {
        $build_icm_cmd .= " -r";
    }

$build_icm_cmd .= " $ref_file.icm < $ref_file.train";

############################################################


############################################################
##########glimmer3
############################################################

my $glimmer3_cmd = "glimmer3";

my $glimmer3_o1 = $cgi->param("glimmer3_o1");
$glimmer3_o1 = lc $glimmer3_o1;
    if ($glimmer3_o1 =~ m/([atcg]{3})\s*\,*\s*([atcg]{3})*\s*\,*\s*([atcg]{3})*/) {
        my $codon_list = $1;
        if (defined $2) {
            $codon_list .= ",$2";
            if (defined $3) {
                $codon_list .= ",$3";
            }
        }
        $glimmer3_cmd .= " -A $codon_list";
    }
       
my $glimmer3_o2 = $cgi->param("glimmer3_o2");
    if ($glimmer3_o2 =~ m/(d+\.*d*)/) {
        $glimmer3_cmd .= " -C $1";
    }
   
my $glimmer3_o3 = $cgi->param("glimmer3_o3");
    if ($glimmer3_o3 =~ m/(d+)/) {
        $glimmer3_cmd .= " -g $1";
    }
    else {
        $glimmer3_cmd .= " -g 110";
    }
    
my $glimmer3_o4 = $cgi->param("glimmer3_o4");
    if ($glimmer3_o3 =~ m/(d+)/) {
        $glimmer3_cmd .= " -o $1";
    }
    else {
        $glimmer3_cmd .= " -o 50";
    }
    
my $glimmer3_o5 = $cgi->param("glimmer3_o5");
    if ($glimmer3_o5 =~ m/(d+\.*d*)\s*\,*\s*(d+\.*d*)*\s*\,*\s*(d+\.*d*)*/) {
        my $prob_list = $1;
        if (defined $2) {
            $prob_list .= ",$2";
            if (defined $3) {
                $prob_list .= ",$3";
            }
        }
        $glimmer3_cmd .= " -P $prob_list";
    }
    
my $glimmer3_o6 = $cgi->param("glimmer3_o6");
    if ($glimmer3_o6 =~ m/(d+)/) {
        $glimmer3_cmd .= " -q $1";
    }
  
my $glimmer3_o7 = $cgi->param("glimmer3_o7");
    if ($glimmer3_o7 =~ m/(d+\.*d*)/) {
        $glimmer3_cmd .= " -t $1";
    }
    else {
        $glimmer3_cmd .= " -t 30";
    }
   
my $glimmer3_o8 = $cgi->param("glimmer3_o8");
    if ($glimmer3_o8 =~ m/(d+)/) {
        $glimmer3_cmd .= " -z $1";
    }

my $glimmer3_o9 = $cgi->param("glimmer3_o9");
$glimmer3_o9 = lc $glimmer3_o9;
    if ($glimmer3_o9 =~ m/([atcg]{3})\s*\,*\s*([atcg]{3})*\s*\,*\s*([atcg]{3})*/) {
        my $codon_list = $1;
        if (defined $2) {
            $codon_list .= ",$2";
            if (defined $3) {
                $codon_list .= ",$3";
            }
        }
        $glimmer3_cmd .= " -Z $codon_list";
    }
       
my $glimmer3_s1 = $cgi->param("glimmer3_s1");
    if ($glimmer3_s1 eq "1") {
        $glimmer3_cmd .= " -f";
    }
    
my $glimmer3_s2 = $cgi->param("glimmer3_s2");
    if ($glimmer3_s2 eq "1") {
        $glimmer3_cmd .= " -l";
    }
    
my $glimmer3_s3 = $cgi->param("glimmer3_s3");
    if ($glimmer3_s3 eq "1") {
        $glimmer3_cmd .= " -M";
    }
    
my $glimmer3_s4 = $cgi->param("glimmer3_s4");
    if ($glimmer3_s4 eq "1") {
        $glimmer3_cmd .= " -r";
    }
    
my $glimmer3_s5 = $cgi->param("glimmer3_s5");
    if ($glimmer3_s5 eq "1") {
        $glimmer3_cmd .= " -X";
    }
    

$glimmer3_cmd .= " $query_file.fasta $ref_file.icm $query_file";

############################################################


############################################################
##########Run shell commands
############################################################

my $extract1_cmd = "extract -t $ref_file.fasta $ref_file.longorfs > $ref_file.train";
my $extract2_cmd = "extract -t $query_file.fasta $query_file.predict > $query_file.glimmer";

my $shellcmd = 'PATH=$PATH:/var/www/bmouler/final/glimmer3/bin && cd /var/www/bmouler/final/uploads && '."$long_orfs_cmd && $extract1_cmd && $build_icm_cmd && $glimmer3_cmd && $extract2_cmd";
system($shellcmd);

############################################################


############################################################
##########Parse the results
############################################################

open (INFILE, "</var/www/bmouler/final/uploads/$query_file.glimmer");

my @orf;
my @start;
my @finish;
my @length;
my @sequence;
my $n = "";

while (<INFILE>) {
	if (m/>(orf\d+)\s+(\d+)\s+(\d+)\s+len=(\d+)/) {
		push @orf, $1;
		push @start, $2;
		push @finish, $3;
		push @length, $4;
		push @sequence, $n;
		$n = "";
	}
	elsif (m/([ATCG]+)/i) {
		$n .= $1;
	}
} push @sequence, $n;

shift @sequence;

close(INFILE);

############################################################


############################################################
##########Compute statistics
############################################################

my @weight;
my @countA;
my @countC;
my @countG;
my @countT;
my @GCcontent;
my $gene_count = scalar(@orf);

for (my $i = 0; $i < scalar(@orf); $i++) {
    my $seq_obj = Bio::Seq->new(-seq => lc($sequence[$i]), -alphabet => 'dna' );
    my $seq_stats  = Bio::Tools::SeqStats->new($seq_obj);
    my $weight = $seq_stats->get_mol_wt();
    my $hash_ref = $seq_stats->count_monomers();
    
    push @weight, $$weight[0];
    my $A = $hash_ref->{"A"};
    push @countA, $hash_ref->{"A"};
    my $C = $hash_ref->{"C"};
    push @countC, $hash_ref->{"C"};
    my $G = $hash_ref->{"G"};
    push @countG, $hash_ref->{"G"};
    my $T = $hash_ref->{"T"};
    push @countT, $hash_ref->{"T"};
    
    my $gc = (($C+$G)/($A+$T+$C+$G)*100);
    if ($gc =~ m/(d*\.d{4})d*/) {
        $gc = "$1";
    }
           
    push @GCcontent, $gc;
}

############################################################


############################################################
##########Print results to tab-delimited text file for SQL
############################################################

open (OUTFILE, ">/var/www/bmouler/final/uploads/$query_file.txt");
my($day, $month, $year)=(localtime)[3,4,5];

for (my $i=0; $i<scalar(@orf); $i++) {
    print OUTFILE "$year$day$month\_$query_file\_$orf[$i]\t$orf[$i]\t$start[$i]\t$finish[$i]\t$length[$i]\t$weight[$i]\t$countA[$i]\t$countC[$i]\t$countG[$i]\t$countT[$i]\t$GCcontent[$i]\t$sequence[$i]\n";
}

close OUTFILE;

############################################################


############################################################
##########Push results to HTML template
############################################################

#Create data structure for table in HTML template
my @table;
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
$template -> param(TABLE => \@table );

$template->param(GENECOUNT => "$gene_count");
$template->param(CMD1 => "$long_orfs_cmd");
$template->param(CMD2 => "$extract1_cmd");
$template->param(CMD3 => "$build_icm_cmd");
$template->param(CMD4 => "$glimmer3_cmd");
$template->param(CMD5 => "$extract2_cmd");
$template->param(FILENAME => "$query_file");
$template->param(SEARCHID => "$year$day$month\_$query_file");

print $cgi -> header('text/html');
print $template->output;

############################################################