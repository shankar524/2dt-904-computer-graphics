in vec2 position;

uniform vec2 resolution;

void main() {
    float u_margin = 0.001;

    vec2 finalPosition = position;

    float aspect = resolution.x / resolution.y;

    // Apply margin with aspect ratio correction
    vec2 margin = vec2(u_margin / aspect, u_margin);

    // Adjust positions based on margin
    finalPosition = mix(
        finalPosition,
        clamp(finalPosition, -1.0 + margin, 1.0 - margin),
        step(abs(finalPosition), vec2(1.0))
    );

    gl_Position = vec4(finalPosition, 0.0, 1.0);
}
