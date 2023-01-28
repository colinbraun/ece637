#include "util.h"

double ***get_color_image(size_t width, size_t height) {
    void **red = get_img(width, height, sizeof(double));
    void **green = get_img(width, height, sizeof(double));
    void **blue = get_img(width, height, sizeof(double));
    void ***pppt = malloc(3*sizeof(void*));
    pppt[0] = red;
    pppt[1] = green;
    pppt[2] = blue;
    return (double ***)pppt;
}

void free_color_image(void ***img) {

    free_img(img[0]);
    free_img(img[1]);
    free_img(img[2]);
    free(img);
}

int clip_color_image(double ***img, size_t width, size_t height) {
    // Clip the color image's values to be between 0 and 255
    // Returns 0 if the image was not changed, 1 otherwise

    int clip_required = 0;
    for (int color = 0; color < 3; color++) {
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                if (img[color][row][col] > 255) {
                    img[color][row][col] = 255;
                    clip_required = 1;
                }
                else if (img[color][row][col] < 0) {
                    img[color][row][col] = 0;
                    clip_required = 1;
                }
            }
        }
    }

    return clip_required;

}

void save_color_image_to_tiff(double ***img, size_t width, size_t height, char *filename) {
    // First clip the image
    clip_color_image(img, width, height);
    struct TIFF_img image;
    get_TIFF ( &image, height, width, 'c' );
    for (int color = 0; color < 3; color++) {
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                image.color[color][row][col] = img[color][row][col];
            }
        }
    }

    FILE *fp;
    /* open image file */
    if ( ( fp = fopen ( filename, "wb" ) ) == NULL ) {
        fprintf ( stderr, "cannot open file %s\n", filename);
        exit ( 1 );
    }
        
    /* write image */
    if ( write_TIFF ( fp, &image ) ) {
        fprintf ( stderr, "error writing TIFF file %s\n", filename);
        exit ( 1 );
    }
        
    /* close image file */
    fclose ( fp );

}

// Returns the convolution of a 2D signal with a 2D impulse response. This must be freed with free_img()
// `img` is the input image, `width` is the width of the input image, `height`is the height of the input image,
// `h` is the filter to convolve with, `h_width` is the width of the filter, `h_height` is the height of the filter.
double **convolve(double **img, size_t width, size_t height, double **h, size_t h_width, size_t h_height) {
    // Create the resulting image buffer
    double **result = (double **)get_img(width, height, sizeof(double));
    // find center position of kernel (half of kernel size)
    int kCenterX = h_width / 2;
    int kCenterY = h_height / 2;

    for (int i = 0; i < height; ++i)              // rows
    {
        printf("Convolving row %d", i);
        for (int j = 0; j < width; ++j)          // columns
        {
            for (int m = 0; m < h_height; ++m)     // kernel rows
            {
                int mm = h_height - 1 - m;      // row index

                for (int n = 0; n < h_width; ++n) // kernel columns
                {
                    int nn = h_width - 1 - n;  // column index

                    // index of input signal, used for checking boundary
                    int ii = i + (m - kCenterY);
                    int jj = j + (n - kCenterX);

                    // ignore input samples which are out of bound
                    if (ii >= 0 && ii < height && jj >= 0 && jj < width)
                        result[i][j] += img[ii][jj] * h[mm][nn];
                }
            }
        }
    }
    return result;
}

// Convert a TIFF_img to a colored image data of doubles
double ***tiff_to_double(struct TIFF_img *tiff_img) {
    int32_t width = tiff_img->width;
    int32_t height = tiff_img->height;
    double ***result = get_color_image(width, height);
    for (int color = 0; color < 3; color++) {
        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                result[color][i][j] = (double)(tiff_img->color[color][i][j]);
            }
        }
    }
    return result;
}

void save_grayscale_image_to_tiff(double **img, size_t width, size_t height, char *filename)
{

}
// unsigned char type image of the above version of the above
void save_grayscale_image_to_tiff_c(unsigned char **img, size_t width, size_t height, char *filename)
{
    struct tiff_img image;
    get_tiff ( &image, height, width, 'c' );
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                image.mono[row][col] = img[row][col];
            }
        }

    file *fp;
    /* open image file */
    if ( ( fp = fopen ( filename, "wb" ) ) == null ) {
        fprintf ( stderr, "cannot open file %s\n", filename);
        exit ( 1 );
    }
        
    /* write image */
    if ( write_tiff ( fp, &image ) ) {
        fprintf ( stderr, "error writing tiff file %s\n", filename);
        exit ( 1 );
    }
        
    /* close image file */
    fclose ( fp );

}