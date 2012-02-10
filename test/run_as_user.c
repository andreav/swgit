#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main( int argc, char ** argv )
{
  if( argc != 3 )
    return 1;

  int uid = atoi( argv[1] );
  setuid( uid );
  system( argv[2] );

  return 0;
}

