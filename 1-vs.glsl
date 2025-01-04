uniform mat4 mModel;
uniform mat4 mProjView;

in vec3 position;
in vec3 vertexColor;


out vec3 fragPos;
out vec3 normal;
out vec3 color;

void main()
{
  fragPos = vec3(mModel * vec4(position, 1.0));
  normal = mat3(transpose(inverse(mModel))) * normal;
  color = vertexColor;

  gl_Position = mProjView * mModel * vec4(position, 1.0);
}
