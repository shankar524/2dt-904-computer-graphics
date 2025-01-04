in vec3 color;
in vec3 fragPos;

out vec4 fragColor;

uniform vec3 lightPos; // Position of the light source (Sun)
uniform vec3 viewPos;  // Position of the camera/viewer
uniform vec3 lightColor; // Color of the light

uniform float ambientStrength;
uniform float diffuseStrength;
uniform float specularStrength;
uniform float shininess;
uniform bool emitsLight; // Indicates if the celestial body emits light

void main() {
  if(emitsLight) {
    fragColor = vec4(color, 1.0);
  } else {
    // Ambient
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse
    vec3 norm = normalize(fragPos); // Use fragPos as the normal for a unit sphere
    vec3 lightDir = normalize(lightPos - fragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diffuseStrength * diff * lightColor;

    // Specular
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor;

    // Combine results
    vec3 result = (ambient + diffuse + specular) * color;
    fragColor = vec4(result, 1.0);
  }
}
