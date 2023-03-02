// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "nxp_cup_interfaces/msg/detail/pixy_vector__struct.h"
#include "nxp_cup_interfaces/msg/detail/pixy_vector__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool nxp_cup_interfaces__msg__pixy_vector__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[47];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("nxp_cup_interfaces.msg._pixy_vector.PixyVector", full_classname_dest, 46) == 0);
  }
  nxp_cup_interfaces__msg__PixyVector * ros_message = _ros_message;
  {  // timestamp
    PyObject * field = PyObject_GetAttrString(_pymsg, "timestamp");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->timestamp = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }
  {  // m0_x0
    PyObject * field = PyObject_GetAttrString(_pymsg, "m0_x0");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m0_x0 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m0_y0
    PyObject * field = PyObject_GetAttrString(_pymsg, "m0_y0");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m0_y0 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m0_x1
    PyObject * field = PyObject_GetAttrString(_pymsg, "m0_x1");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m0_x1 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m0_y1
    PyObject * field = PyObject_GetAttrString(_pymsg, "m0_y1");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m0_y1 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m1_x0
    PyObject * field = PyObject_GetAttrString(_pymsg, "m1_x0");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m1_x0 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m1_y0
    PyObject * field = PyObject_GetAttrString(_pymsg, "m1_y0");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m1_y0 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m1_x1
    PyObject * field = PyObject_GetAttrString(_pymsg, "m1_x1");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m1_x1 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // m1_y1
    PyObject * field = PyObject_GetAttrString(_pymsg, "m1_y1");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->m1_y1 = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * nxp_cup_interfaces__msg__pixy_vector__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of PixyVector */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("nxp_cup_interfaces.msg._pixy_vector");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "PixyVector");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  nxp_cup_interfaces__msg__PixyVector * ros_message = (nxp_cup_interfaces__msg__PixyVector *)raw_ros_message;
  {  // timestamp
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->timestamp);
    {
      int rc = PyObject_SetAttrString(_pymessage, "timestamp", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m0_x0
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m0_x0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m0_x0", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m0_y0
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m0_y0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m0_y0", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m0_x1
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m0_x1);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m0_x1", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m0_y1
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m0_y1);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m0_y1", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m1_x0
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m1_x0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m1_x0", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m1_y0
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m1_y0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m1_y0", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m1_x1
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m1_x1);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m1_x1", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // m1_y1
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->m1_y1);
    {
      int rc = PyObject_SetAttrString(_pymessage, "m1_y1", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
