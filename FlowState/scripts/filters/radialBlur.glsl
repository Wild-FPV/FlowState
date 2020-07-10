uniform sampler2D bgl_RenderedTexture;

vec2 texcoord = vec2(gl_TexCoord[0]).st;
vec2 cancoord = vec2(gl_TexCoord[3]).st;

#define KERNEL_SIZE 3.0
#define blurclamp 0.002
#define bias 0.01

void main(void)
{
	//float f = 0.7;  // focal length

	//float ox = 0.5; // center, x axis

	//float oy = 0.5; // center, y axis

	//float scale = 0.541; // texture scale

	//float f = 0.6;  // focal length
    float f = 1;  // focal length

	float ox = 0.5; // center, x axis

	float oy = 0.5; // center, y axis

	//float scale = .581;//41; // texture scale
    float scale = 1.0;//41; // texture scale

    vec4 col = vec4( 0, 0, 0, 0 );
    vec4 initColor = texture2D(bgl_RenderedTexture, texcoord.st);
    float iterations = 5;
    for ( float x = 0; x < iterations; x += 1.0 )
    {
       float k1 = 0.01*x;    // constant for radial distortion correction

    	float k2 = 0.01*x;



    	vec2 xy = (texcoord.st - vec2(ox, oy))/vec2(f,f) * scale;



    	vec2 r = vec2 (sqrt( dot(xy, xy) ));

    	float r2 = float (r * r);

    	float r4 = r2 * r2;

    	float coeff = (k1 * r2 + k2 * r4); 

    	xy = ((xy + xy * coeff) * f) + vec2(ox, oy);
        initColor+=texture2D(bgl_RenderedTexture, xy);
    }
    initColor/=iterations;
	
	
	
	gl_FragColor = initColor;//((texture2D(bgl_RenderedTexture, texcoord.st)*.5)+(texture2D(bgl_RenderedTexture, xy)*.5));
	
}