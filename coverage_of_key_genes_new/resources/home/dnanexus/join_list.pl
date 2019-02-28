$l1 = shift;
$l2 = shift;

open (L2,"$l2");
while (<L2>){
    if (/(\S+)\s+(.+)$/){
	$info{$1} = $2;
    }
}

open (L1,"$l1");
while (<L1>){
    if (/(\S+)\s+(.+)$/){
	if ($info{$1}){
	    print "$1\t$2\t$info{$1}\n";
	}
    }else{
	print STDERR "No info for $1 from $l1\n";
    }
}

