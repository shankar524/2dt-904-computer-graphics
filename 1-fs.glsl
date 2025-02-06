in vec3 fragPos;
in vec3 normal;
in vec3 color;

out vec4 fragColor;

uniform vec3 lightPosition;
uniform vec3 viewPos;
uniform vec3 lightColor;

uniform float ambientStrength;
uniform float diffuseStrength;
uniform float shininess;
uniform bool emitsLight;

void main() {
    vec3 ambient;
    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);
    vec3 lightDir = normalize(lightPosition - fragPos);

    if (emitsLight) {
        // multiply ambience for light source
        ambient = 10 * ambientStrength * lightColor;
    } else {
        float diff = max(dot(normal, lightDir), 0.0);
        // Ambient
        ambient = ambientStrength * lightColor;

        // Diffuse
        diffuse = diffuseStrength * diff * lightColor;

        // Specular
        if(diff > 0.0) {
            vec3 viewDir = normalize(viewPos - fragPos);
            vec3 reflectDir = reflect(-lightDir, normal);
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), 8);
            specular = shininess * spec * lightColor;
        }
    }

    // Combine results
    vec3 result = ambient + diffuse + specular;
    fragColor = vec4(result * color, 1.0);
}
