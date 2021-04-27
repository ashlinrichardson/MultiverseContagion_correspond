#define STR_MAX 1000
#include "newzpr.h"
#include "pthread.h"
#include "time.h"
#include "vec3d.h"
#define MYFONT GLUT_BITMAP_HELVETICA_12
#include <stdio.h>
#include <stdlib.h>
#include"misc.h"
#include<unordered_set>

#define SPHERE_SIZE 1.

/* Where the simulation data will go */
vector<str> my_lines; // ssv data
vector<int> infected;
vector<int> infector;
map<int, int> my_infector;
map<int, int> infection_gen;
unordered_set<int> connected;

vector<float> ball_x;
vector<float> ball_y;
vector<float> ball_z;

/* Draw axes */
int SHIFT_KEY;
#define STARTX 700
#define STARTY 700
int fullscreen;
clock_t start_time;
clock_t stop_time;
#define SECONDS_PAUSE 0.4
char console_string[STR_MAX];
int console_position;
int renderflag;

void _pick(GLint name){
  cout << "PickSet:";
  std::set<GLint>::iterator it;
  for(it=myPickNames.begin(); it!=myPickNames.end(); it++){
    cout << *it << "," ;
  }
  cout << endl;
  fflush(stdout);
}

void renderBitmapString(float x, float y, void *font, char *string){
  char *c;
  glRasterPos2f(x,y);
  for (c=string; *c != '\0'; c++){
    glutBitmapCharacter(font, *c);
  }
}

//http://www.codeproject.com/Articles/80923/The-OpenGL-and-GLUT-A-Powerful-Graphics-Library-an
void setOrthographicProjection(){
  int h = WINDOWY;
  int w = WINDOWX;
  glMatrixMode(GL_PROJECTION);
  glPushMatrix();
  glLoadIdentity();
  gluOrtho2D(0, w, 0, h);
  glScalef(1, -1, 1);
  glTranslatef(0, -h, 0);
  glMatrixMode(GL_MODELVIEW);
}

void resetPerspectiveProjection(){
  glMatrixMode(GL_PROJECTION);
  glPopMatrix();
  glMatrixMode(GL_MODELVIEW);
}

void drawText(){
  glColor3f(0.0f,1.0f,0.0f);
  setOrthographicProjection();
  glPushMatrix();
  glLoadIdentity();
  int lightingState = glIsEnabled(GL_LIGHTING);
  glDisable(GL_LIGHTING);
  renderBitmapString(3,WINDOWY-3,(void *)MYFONT,console_string);
  if(lightingState) glEnable(GL_LIGHTING);
  glPopMatrix();
  resetPerspectiveProjection();
}

float a1, a2, a3;

class point{
  public:
  point(){
  }
};

void drawArrow(vec3d x1, vec3d x2){
  /* y1, y2-- start and end positions at which to plot arrow.. */
  //vec3d x1(y1);
  //vec3d x2(y2);
  float arrowLength = SPHERE_SIZE;
  float takeOff = 0.;
  vec3d Mx1(x1);//-rx);//(parentglWindow->rX)); //arrow start vector..
  vec3d Mx2(x2);//-rx);//(parentglWindow->rX));//..arrow end vector.
  vec3d dx(Mx2-Mx1);
  float len = dx.length();
  vec3d dxS( dx / len);
  float beginAtSize = 0.;//parentglWindow->sphereSize;
  Mx1 = Mx1 + (dxS * beginAtSize);

  /* the arrow line */
  glLineWidth(1.);
  glPushMatrix();
  glBegin(GL_LINES);
  Mx1.vertex(); Mx2.vertex();
  glEnd();
  glPopMatrix();
  //if(pushName) glPopName();

  /* the arrow head */
  dx= dx *((len-takeOff)/len);
  len = dx.length();
  Mx2 = (Mx1+dx);
  float tPL = arrowLength;

  /*arrow head base point*/
  vec3d tx( dx - (dx*(tPL/len)));
  vec3d normalV( -dx.y, dx.x, 0.);
  normalV = normalV / normalV.length();
  float tNormal = (arrowLength/ 2.);
  vec3d leftP( tx + ( normalV*tNormal));
  vec3d rightP( tx - ( normalV*tNormal));
  vec3d nV2( tx.cross(normalV));
  nV2 = nV2 / nV2.length();
  vec3d leftP2( tx + ( nV2*tNormal));
  vec3d rightP2( tx - ( nV2*tNormal));

  glPushMatrix();
  glTranslatef(Mx1.x, Mx1.y, Mx1.z);
  glBegin(GL_TRIANGLES);
  tx.vertex(); leftP.vertex(); dx.vertex();
  glEnd();
  glPopMatrix();

  glPushMatrix();
  glTranslatef(Mx1.x, Mx1.y, Mx1.z);
  glBegin(GL_TRIANGLES);
  tx.vertex(); rightP.vertex(); dx.vertex();
  glEnd();
  glPopMatrix();

  glPushMatrix();
  glTranslatef(Mx1.x, Mx1.y, Mx1.z);
  glBegin(GL_TRIANGLES);
  tx.vertex(); leftP2.vertex(); dx.vertex();
  glEnd();
  glPopMatrix();

  glPushMatrix();
  glTranslatef(Mx1.x, Mx1.y, Mx1.z);
  glBegin(GL_TRIANGLES);
  tx.vertex(); rightP2.vertex(); dx.vertex();
  glEnd();
  glPopMatrix();
}

void drawAxes(void){
  /* Name-stack manipulation for the purpose of
  selection hit processing when mouse button
  is pressed. Names are ignored in normal
  OpenGL rendering mode. */
  int i, N;
  N = ball_x.size();

  for0(i, N){
    if(connected.count(i)){
    glPushMatrix();
    glPushName(i);
    glTranslatef( ball_x[i], ball_y[i], ball_z[i]);
    glColor3f(1,1,0);

    if(myPickNames.count(i)) glColor3f(0,1,1);

    glutSolidSphere(SPHERE_SIZE, 8,8 );
    glPopName();
    glPopMatrix();
    }
  }

  glColor3f(0,1,1);
  for(map<int, int>::iterator it = my_infector.begin(); it != my_infector.end(); it++){
    int infected_j = it->first;
    int infector_j = it->second;
    vec3d src(ball_x[infector_j], ball_y[infector_j], ball_z[infector_j]);
    vec3d dst(ball_x[infected_j], ball_y[infected_j], ball_z[infected_j]);
    drawArrow(src, dst);
  }
}

/* Callback function for drawing */
void display(void){
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  drawAxes();
  //glutSwapBuffers();//Flush();
  drawText();
  //glutPostRedisplay();
  //glFlush();
  glutSwapBuffers();

  renderflag = false;
}

/* Callback function for pick-event handling from ZPR */

void quitme(){
  exit(0);
}

/* Keyboard functions */
void keyboard(unsigned char key, int x, int y){
  printf("key: %c %d\n", key, (int)key);
  switch(key){
    // Backspace

    /*case GLUT_F1:
    //if( stop_time > clock())
    // break;
    if(!fullscreen){
      fullscreen=1;
      glutFullScreen();
    }
    else{
      fullscreen=0;
      glutReshapeWindow(STARTX, STARTY);
      glutPositionWindow(0, 0);
    }
    glutPostRedisplay();
    //display();
    //start_time = clock();
    //stop_time = start_time + CLOCKS_PER_SEC;
    //while(clock() < stop_time){
    //}

    break;
    */

    case 8 :
    case 127:
    if(console_position>0){
      console_position --;
      console_string[console_position]='\0';
      printf("STRING: %s\n", &console_string[0]);
      //printf( "%d Pressed Backspace\n",(char)key);
      display();
    }
    break;

    // Enter
    case 13 :
    //printf( "%d Pressed RETURN\n",(char)key);
    console_string[0]='\0';
    console_position=0;
    display();
    break;

    // Escape
    case 27 :
    quitme();
    exit(0);
    //printf( "%d Pressed Esc\n",(char)key);
    break;

    // Delete
    /* case 127 :
    printf( "%d Pressed Del\n",(char)key);
    break;
    */
    default:
    //printf( "Pressed key %c AKA %d at position %d % d\n",(char)key, key, x, y);
    console_string[console_position++] = (char)key;
    console_string[console_position]='\0';
    printf("STRING: %s\n", &console_string[0]);
    display();
    break;
  }
}

/* Keyboard functions */
void special(int key, int x, int y){
  printf("special key: %c %d\n", (char)key, (int)key);
  if(key ==112){
    SHIFT_KEY = !SHIFT_KEY;
    cout << "SHIFT " << SHIFT_KEY << endl;
  }

}

static GLfloat light_ambient[] = {
0.0, 0.0, 0.0, 1.0 };
static GLfloat light_diffuse[] = {
1.0, 1.0, 1.0, 1.0 };
static GLfloat light_specular[] = {
1.0, 1.0, 1.0, 1.0 };
static GLfloat light_position[] = {
1.0, 1.0, 1.0, 0.0 };

static GLfloat mat_ambient[] = {
0.7, 0.7, 0.7, 1.0 };
static GLfloat mat_diffuse[] = {
0.8, 0.8, 0.8, 1.0 };
static GLfloat mat_specular[] = {
1.0, 1.0, 1.0, 1.0 };
static GLfloat high_shininess[] = {
100.0 };

// https://computing.llnl.gov/tutorials/pthreads/

void idle(){
  if( renderflag ){
    glFlush();
    glutPostRedisplay();
  }
}

int main(int argc, char *argv[]){
  SHIFT_KEY = false;
  vector<vector<string>> output;
  FILE * f = fopen(argv[1], "rb");
  char buffer[2048];
  char * buf = &buffer[0];
  size_t bs = 2048;

  int maxI = 0;
  while(getline(&buf, &bs, f) > 0){
    str line(buffer);
    trim(line);
    vector<str> words(split(line, ' '));
    cout << words << endl;
    str line_infected(words[2]);
    str line_infector(words[5]);
    str line_gen(words[7]);

    vector<str> w_infected(split(line_infected, ':'));
    vector<str> w_infector(split(line_infector, ':'));

    cout << w_infector[0] << " -> " << w_infected[0] << endl;
    int infector_i = atoi(w_infector[0].c_str());
    int infected_i = atoi(w_infected[0].c_str());
    infector.push_back(infector_i);
    infected.push_back(infected_i);
    connected.insert(infector_i);
    connected.insert(infected_i);

    if(infector_i > maxI) maxI = infector_i;
    if(infected_i > maxI) maxI = infected_i;
    my_infector[infected_i] = infector_i;

    my_lines.push_back(line);
    my_line[infected_i] = line;

    infection_gen[infected_i] = atoi(&((line_gen.c_str())[3]));
  }
  int i;
  for0(i, maxI + 1){
    ball_x.push_back((float)i);
    int inf_i = i;

    if(my_infector.count(i) > 0) inf_i = my_infector[i];

    ball_y.push_back((float)(inf_i));
    ball_z.push_back((float)infection_gen[infected[i]]);
  }

  pick = _pick;
  printf("main()\n");
  renderflag = false;
  a1=a2=a3=1;
  console_position = 0;
  //Py_Initialize();
  //printf("Py_init()\n");

  fullscreen=0;

  /* Initialise olLUT and create a window */

  printf("try glut init...\n");

  glutInit(&argc, argv);
  printf("glutInit()\n");

  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowSize(STARTX,STARTY);
  glutCreateWindow("");
  zprInit();

  printf("glutCreateWindow()\n");

  /* Configure GLUT callback functions */

  glutDisplayFunc(display);
  glutKeyboardFunc(keyboard);
  glutSpecialFunc(special);
  glutSpecialUpFunc(special);
  // glutKeyboardUpFunc(keyboardup);

  glutIdleFunc(idle);

  glScalef(0.25,0.25,0.25);

  /* Configure ZPR module */
  // zprInit();
  zprSelectionFunc(drawAxes); /* Selection mode draw function */
  zprPickFunc(pick); /* Pick event client callback */

  /* Initialise OpenGL */

  glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
  glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
  glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
  glLightfv(GL_LIGHT0, GL_POSITION, light_position);

  glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient);
  glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse);
  glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
  glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess);

  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);
  glDepthFunc(GL_LESS);
  glEnable(GL_DEPTH_TEST);
  glEnable(GL_NORMALIZE);
  glEnable(GL_COLOR_MATERIAL);

  // pthread_t thread;
  // pthread_create(&thread, NULL, &threadfun, NULL);
  /* Enter GLUT event loop */
  glutMainLoop();
  return 0;
}
