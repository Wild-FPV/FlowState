uniform sampler2D bgl_RenderedTexture;

vec2 texcoord = vec2(gl_TexCoord[0]).st;
out vec4 FinalColor;

void main(void)
{
	float Pixels = 600.0;
    float dx = 1.00 * (1.0 / Pixels);
    float dy = 1.20 * (1.0 / Pixels);
    vec2 Coord = vec2(dx * floor(texcoord.x / dx),
                      dy * floor(texcoord.y / dy));
    gl_FragColor = texture(bgl_RenderedTexture, Coord);
}