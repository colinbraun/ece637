
#include <math.h>
#include <tiff.h>
#include <allocate.h>
#include <randlib.h>
#include <typeutil.h>

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img;
  int32_t i,j;

  if ( argc != 2 ) error( argv[0] );

  /* open image file */
  if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file %s\n", argv[1] );
    exit ( 1 );
  }

  /* read image */
  if ( read_TIFF ( fp, &input_img ) ) {
    fprintf ( stderr, "error reading file %s\n", argv[1] );
    exit ( 1 );
  }

  /* close image file */
  fclose ( fp );

  /* check the type of image data */
  if ( input_img.TIFF_type != 'c' ) {
    fprintf ( stderr, "error:  image must be 24-bit color\n" );
    exit ( 1 );
  }

  //----------------------SMOOOTHED IMAGE---------------------------
  // Create the image we want
  struct TIFF_img smoothed_image;
  get_TIFF ( &smoothed_image, input_img.height, input_img.width, 'c' );
  /* Filter image along horizontal direction */
  for ( i = 4; i < input_img.height-4; i++ )
  for ( j = 4; j < input_img.width-4; j++ ) {
    int total_red = 0;
    int total_green = 0;
    int total_blue  = 0;
    for (int dx = -4; dx <= 4; dx++) {
        for (int dy = -4; dy <= 4; dy++) {
          total_red += input_img.color[0][i+dy][j+dx];
          total_green += input_img.color[1][i+dy][j+dx];
          total_blue += input_img.color[2][i+dy][j+dx];
        }
    }
    smoothed_image.color[0][i][j] = total_red / 81;
    smoothed_image.color[1][i][j] = total_green / 81;
    smoothed_image.color[2][i][j] = total_blue / 81;
  }

  /* open final image file */
  if ( ( fp = fopen ( "smoothed.tif", "wb" ) ) == NULL ) {
      fprintf ( stderr, "cannot open file smoothed.tif\n");
      exit ( 1 );
  }
    
  /* write smoothed image */
  if ( write_TIFF ( fp, &smoothed_image ) ) {
      fprintf ( stderr, "error writing TIFF file %s\n", argv[2] );
      exit ( 1 );
  }
    
  /* close smoothed image file */
  fclose ( fp );
}

void error(char *name)
{
    printf("usage:  %s  image.tiff \n\n",name);
    printf("this program reads in a 24-bit color TIFF image.\n");
    printf("It then horizontally filters the green component, adds noise,\n");
    printf("and writes out the result as an 8-bit image\n");
    printf("with the name 'green.tiff'.\n");
    printf("It also generates an 8-bit color image,\n");
    printf("that swaps red and green components from the input image");
    exit(1);
}
