#include <Python.h>
#include <complex.h>

int
time_to_infinity(double complex z, double complex c) {
	double complex z_n = z;
	for (int i=0; i < 100; i++) {
		z_n = z_n * z_n + c;
		if (cabs(z_n) > 2.0) {
			return i;
		}
		
	}
	return -1;
}

 
static PyObject*
number_in_julia_set(PyObject* self, PyObject* args)
{
    Py_complex z, c;
 
    if (!PyArg_ParseTuple(args, "DD", &z, &c))
        return NULL;
	
	double complex z_val = z.real + z.imag * I;
	double complex c_val = c.real + c.imag * I;
	int result = time_to_infinity(z_val, c_val);
	if (result == -1) {
		Py_RETURN_TRUE;
	}
	
    return Py_BuildValue("i", result);
}

static PyMethodDef FibMethods[] = {
    {"number_in_julia_set", number_in_julia_set, METH_VARARGS, "Calculate the Fibonacci numbers."},
    {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initjulia(void)
{
    (void) Py_InitModule("julia", FibMethods);
}