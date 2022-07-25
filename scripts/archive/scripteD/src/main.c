#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *ext_div(PyObject *self,PyObject *args){
  double result = 0.0;
  int a,b;
  if(!PyArg_ParseTuple(args,"ii:divide",&a,&b)){
    perror("parse failed!");
    return NULL;
  }
  result = (double)a/(double)b;
  return PyFloat_FromDouble(result);
}

static PyMethodDef EmbMethods[] = {
    {"divide", ext_div,METH_VARARGS,"Low level division in C!"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef dividerModule = {
    PyModuleDef_HEAD_INIT, "divide", NULL, -1, EmbMethods,
    NULL, NULL, NULL, NULL
};

static PyObject *PyInit_divider(void){
    return PyModule_Create(&dividerModule);
}

int main(int argc, char *argv[]) {
  PyObject *pName, *pModule, *pFunc;
  PyObject *pArgs, *pValue;
  int i;

  if (argc < 3) {
    fprintf(stderr, "Usage: <binary> pythonscript funcname [args]\n");
    return 1;
  }
  PyImport_AppendInittab("div", &PyInit_divider);
  Py_Initialize();
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append(\".\")");
  pName = PyUnicode_DecodeFSDefault(argv[1]);
  if(pName == NULL){
    perror("Invalid pName");
    return 1;
  }
  pModule = PyImport_Import(pName);
  Py_DECREF(pName);

  if (pModule != NULL) {
    pFunc = PyObject_GetAttrString(pModule, argv[2]);
    /* pFunc is a new reference */
    if (pFunc && PyCallable_Check(pFunc)) {
      pArgs = PyTuple_New(argc - 3);
      for (i = 0; i < argc - 3; ++i) {
        pValue = PyLong_FromLong(atoi(argv[i + 3]));
        if (!pValue) {
          Py_DECREF(pArgs);
          Py_DECREF(pModule);
          fprintf(stderr, "Cannot convert argument\n");
          return 1;
        }
        /* pValue reference stolen here: */
        PyTuple_SetItem(pArgs, i, pValue);
      }
      pValue = PyObject_CallObject(pFunc, pArgs);
      Py_DECREF(pArgs);
      if (pValue != NULL) {
        printf("Result of call: %f\n", PyFloat_AsDouble(pValue));
        Py_DECREF(pValue);
      } else {
        Py_DECREF(pFunc);
        Py_DECREF(pModule);
        PyErr_Print();
        fprintf(stderr, "Call failed\n");
        return 1;
      }
    } else {
      if (PyErr_Occurred())
        PyErr_Print();
      fprintf(stderr, "Cannot find function \"%s\"\n", argv[2]);
    }
    Py_XDECREF(pFunc);
    Py_DECREF(pModule);
  } else {
    PyErr_Print();
    fprintf(stderr, "Failed to load \"%s\"\n", argv[1]);
    return 1;
  }
  if (Py_FinalizeEx() < 0) {
    return 120;
  }
  return 0;
}
