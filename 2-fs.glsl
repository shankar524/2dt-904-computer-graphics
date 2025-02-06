uniform vec2 resolution;
uniform vec3 startColor;
uniform vec3 endColor;

out vec4 fragColor;

void main() {
    vec2 normalizedFragCoord = (gl_FragCoord.xy / resolution);

    // Create a more pronounced diagonal gradient
    float blendFactor = (normalizedFragCoord.x + normalizedFragCoord.y) / 2.0;

    // Apply a non-linear function to create a smoother transition
    blendFactor = smoothstep(0.0, 1.0, blendFactor);
    vec3 color = mix(startColor, endColor, blendFactor);
    fragColor = vec4(color, 1.0);
}