#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Std;
use lcmUtil;
no warnings 'once';

my $helpMsg=<<HELP;
  $0 [-h] [-d delimiter]
  -h              # help
  -d delimiter    # delimiter char
HELP

die $helpMsg if !getopts("d:h");
die $helpMsg if $main::opt_h;
$main::opt_d = ',' if !$main::opt_d;

my @rows;
map {$_ =~ s/[\n\r]+$//; my @values = split($main::opt_d, $_, -1); push(@rows, \@values)} <>;
my $colNo = @{$rows[0]};
for (my $i = 0; $i < @rows; ++$i)
{
  die "The input data is not uniform (first line's count is $colNo != " . @{$rows[$i]} . " on line " . (1 + $i) . ")" if $colNo != @{$rows[$i]};
}

for (my $m = 0; $m < @{$rows[0]}; ++$m)
{
    print join($main::opt_d, map {$_->[$m]} @rows), "\n";
}


