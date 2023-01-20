
#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"
#include "util.h"

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img;
  int32_t i, j, pixel;

  if ( argc != 3 ) error( argv[0] );
  double lambda = strtod(argv[2], NULL);
  printf("Lambda: %f\n", lambda);

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

  //----------------------SHARPENED IMAGE---------------------------
  // Create the image we want
  double ***sharpened_data = get_color_image(input_img.width, input_img.height);
  struct TIFF_img sharpened_image;
  get_TIFF ( &sharpened_image, input_img.height, input_img.width, 'c' );
  /* Filter image along horizontal direction */
  for ( i = 2; i < input_img.height-2; i++ )
  for ( j = 2; j < input_img.width-2; j++ ) {
    int total_red = 0;
    int total_green = 0;
    int total_blue  = 0;
    for (int dx = -2; dx <= 2; dx++) {
        for (int dy = -2; dy <= 2; dy++) {
          total_red += input_img.color[0][i+dy][j+dx];
          total_green += input_img.color[1][i+dy][j+dx];
          total_blue += input_img.color[2][i+dy][j+dx];
        }
    }
    int img_red = input_img.color[0][i][j];
    int img_green = input_img.color[1][i][j];
    int img_blue = input_img.color[2][i][j];
    sharpened_data[0][i][j] = img_red + lambda * (img_red - total_red/25);
    sharpened_data[1][i][j] = img_green + lambda * (img_green - total_green/25);
    sharpened_data[2][i][j] = img_blue + lambda * (img_blue - total_blue/25);
  }
  save_color_image_to_tiff(sharpened_data, input_img.width, input_img.height, "sharpened.tif");
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
