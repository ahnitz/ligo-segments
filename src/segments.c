/*
 * Copyright (C) 2006--2008  Kipp C. Cannon
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 3 of the License, or (at your
 * option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */


/*
 * ============================================================================
 *
 *                     Segments Module Component --- Main
 *
 * ============================================================================
 */


#include <Python.h>
#include <segments.h>


/*
 * ============================================================================
 *
 *                           Module Initialization
 *
 * ============================================================================
 */


#define MODULE_DOC "C implementations of the infinity, segment, and segmentlist classes from the segments module."


#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC init__segments(void); /* Silence -Wmissing-prototypes */
PyMODINIT_FUNC init__segments(void)
#else
PyMODINIT_FUNC PyInit___segments(void); /* Silence -Wmissing-prototypes */
PyMODINIT_FUNC PyInit___segments(void)
#endif
{
#if PY_MAJOR_VERSION < 3
	PyObject *module = Py_InitModule3(MODULE_NAME, NULL, MODULE_DOC);
#else
	static struct PyModuleDef modef = {
		PyModuleDef_HEAD_INIT,
		.m_name = MODULE_NAME,
		.m_doc = MODULE_DOC,
		.m_size = -1,
		.m_methods = NULL,
	};
	PyObject *module = PyModule_Create(&modef);
#endif

	if(!module)
		goto done;

	if(PyType_Ready(&segments_Infinity_Type) < 0) {
		Py_DECREF(module);
		module = NULL;
		goto done;
	}

	segments_Segment_Type.tp_base = &PyTuple_Type;
	if(!segments_Segment_Type.tp_hash)
		segments_Segment_Type.tp_hash = PyTuple_Type.tp_hash;
	if(PyType_Ready(&segments_Segment_Type) < 0) {
		Py_DECREF(module);
		module = NULL;
		goto done;
	}

	segments_SegmentList_Type.tp_base = &PyList_Type;
	if(PyType_Ready(&segments_SegmentList_Type) < 0) {
		Py_DECREF(module);
		module = NULL;
		goto done;
	}

	/*
	 * Create infinity class
	 */

	Py_INCREF(&segments_Infinity_Type);
	PyModule_AddObject(module, "infinity", (PyObject *) &segments_Infinity_Type);

	/*
	 * Create positive and negative infinity instances
	 */

	segments_PosInfinity = (segments_Infinity *) _PyObject_New(&segments_Infinity_Type);
	segments_NegInfinity = (segments_Infinity *) _PyObject_New(&segments_Infinity_Type);
	Py_INCREF(segments_PosInfinity);
	Py_INCREF(segments_NegInfinity);
	PyModule_AddObject(module, "PosInfinity", (PyObject *) segments_PosInfinity);
	PyModule_AddObject(module, "NegInfinity", (PyObject *) segments_NegInfinity);

	/*
	 * Create segment class.  Ideally the .tp_hash field would be
	 * initialized along with the other fields in the initializer in
	 * segment.c, but something about PyTuple_Type makes the compiler
	 * unhappy with that.
	 */

	Py_INCREF(&segments_Segment_Type);
	PyModule_AddObject(module, "segment", (PyObject *) &segments_Segment_Type);
	/* uninherit tp_print from tuple class */
#if PY_VERSION_HEX < 0x03090000
	/* FIXME: tp_print was removed in Python 3.9.
	 * Remove this once Python 3.8 reaches end of life. */
	segments_Segment_Type.tp_print = NULL;
#endif

	/*
	 * Create segmentlist class
	 */

	Py_INCREF(&segments_SegmentList_Type);
	PyModule_AddObject(module, "segmentlist", (PyObject *) &segments_SegmentList_Type);

done:
#if PY_MAJOR_VERSION < 3
	return;
#else
	return module;
#endif
}
