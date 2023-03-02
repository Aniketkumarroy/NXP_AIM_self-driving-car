// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice
#include "nxp_cup_interfaces/msg/detail/pixy_vector__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


bool
nxp_cup_interfaces__msg__PixyVector__init(nxp_cup_interfaces__msg__PixyVector * msg)
{
  if (!msg) {
    return false;
  }
  // timestamp
  // m0_x0
  // m0_y0
  // m0_x1
  // m0_y1
  // m1_x0
  // m1_y0
  // m1_x1
  // m1_y1
  return true;
}

void
nxp_cup_interfaces__msg__PixyVector__fini(nxp_cup_interfaces__msg__PixyVector * msg)
{
  if (!msg) {
    return;
  }
  // timestamp
  // m0_x0
  // m0_y0
  // m0_x1
  // m0_y1
  // m1_x0
  // m1_y0
  // m1_x1
  // m1_y1
}

nxp_cup_interfaces__msg__PixyVector *
nxp_cup_interfaces__msg__PixyVector__create()
{
  nxp_cup_interfaces__msg__PixyVector * msg = (nxp_cup_interfaces__msg__PixyVector *)malloc(sizeof(nxp_cup_interfaces__msg__PixyVector));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(nxp_cup_interfaces__msg__PixyVector));
  bool success = nxp_cup_interfaces__msg__PixyVector__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
nxp_cup_interfaces__msg__PixyVector__destroy(nxp_cup_interfaces__msg__PixyVector * msg)
{
  if (msg) {
    nxp_cup_interfaces__msg__PixyVector__fini(msg);
  }
  free(msg);
}


bool
nxp_cup_interfaces__msg__PixyVector__Sequence__init(nxp_cup_interfaces__msg__PixyVector__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  nxp_cup_interfaces__msg__PixyVector * data = NULL;
  if (size) {
    data = (nxp_cup_interfaces__msg__PixyVector *)calloc(size, sizeof(nxp_cup_interfaces__msg__PixyVector));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = nxp_cup_interfaces__msg__PixyVector__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        nxp_cup_interfaces__msg__PixyVector__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
nxp_cup_interfaces__msg__PixyVector__Sequence__fini(nxp_cup_interfaces__msg__PixyVector__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      nxp_cup_interfaces__msg__PixyVector__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

nxp_cup_interfaces__msg__PixyVector__Sequence *
nxp_cup_interfaces__msg__PixyVector__Sequence__create(size_t size)
{
  nxp_cup_interfaces__msg__PixyVector__Sequence * array = (nxp_cup_interfaces__msg__PixyVector__Sequence *)malloc(sizeof(nxp_cup_interfaces__msg__PixyVector__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = nxp_cup_interfaces__msg__PixyVector__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
nxp_cup_interfaces__msg__PixyVector__Sequence__destroy(nxp_cup_interfaces__msg__PixyVector__Sequence * array)
{
  if (array) {
    nxp_cup_interfaces__msg__PixyVector__Sequence__fini(array);
  }
  free(array);
}
