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