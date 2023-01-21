#include <math.h>
#include <tiff.h>
#include <allocate.h>
#include <randlib.h>
#include <typeutil.h>
#include "util.h"

void error(char *name);

int main (int argc, char **argv) 
{
  FILE *fp;
  struct TIFF_img input_img;
  struct TIFF_img filter_img;
  int32_t i, j, pixel;

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

  // // LOAD THE FILTER
  // /* open image file */
  // if ( ( fp = fopen ( "../results/h_out.tif", "rb" ) ) == NULL ) {
  //   fprintf ( stderr, "cannot open filter file\n");
  //   exit ( 1 );
  // }

  // /* read image */
  // if ( read_TIFF ( fp, &filter_img ) ) {
  //   fprintf ( stderr, "error reading file h_out.tif\n");
  //   exit ( 1 );
  // }

  // /* close image file */
  // fclose ( fp );
  //----------------------SECTION 5 IMAGE---------------------------
  // Create the image we want
  double ***result_data = get_color_image(input_img.width, input_img.height);
  double ***input_data = tiff_to_double(&input_img);
  double **filter_data = get_img(256, 256, sizeof(double));
  filter_data[127][127] = 1;
  double filter_sum = 0;
  for (int row = 0; row < 256; row++) {
    for (int col = 0; col < 256; col++) {
      if (row == 0 || col == 0) {
        // Don't start at 0, 0. Will get an index out of bounds.
        continue;
      }
      if (row == 127 && col == 127){
        // Don't clober the data we initialized
        continue;
      }
      filter_data[row][col] = 0.9 * (filter_data[row-1][col] + filter_data[row][col-1]) - 0.81 * filter_data[row-1][col-1];
      filter_sum += filter_data[row][col];
    }
  }
  // Make DC Component gain = 1
  for (int row = 0; row < 256; row++) {
    for (int col = 0; col < 256; col++) {
      filter_data[row][col] /= filter_sum;
    }
  }
  // double ***filter_data = tiff_to_double(&filter_img);
  struct TIFF_img result_image;
  get_TIFF ( &result_image, input_img.height, input_img.width, 'c' );
  /* Filter image along horizontal direction */
  for (int color = 0; color < 3; color++) {
    printf("Performing a convolution");
    result_data[color] = convolve(input_data[color], input_img.width, input_img.height, filter_data, 256, 256);
  }
  // for (int color = 0; color < 3; color++) {
  //   for (int row = 0; row < input_img.height; row++) {
  //     for (int col = 0; col < input_img.width; col++) {
  //       if (row == 0 || col == 0) {
  //         continue;
  //       }
  //       result_data[color][row][col] = 0.9 * (input_data[color][row-1][col] + input_data[color][row][col-1]) - 0.81 * input_data[color][row-1][col-1];
  //     }
  //   }
  // }
  save_color_image_to_tiff(result_data, input_img.width, input_img.height, "section5.tif");


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

