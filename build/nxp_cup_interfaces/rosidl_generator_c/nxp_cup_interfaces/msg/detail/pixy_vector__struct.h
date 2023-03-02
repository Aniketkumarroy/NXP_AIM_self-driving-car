// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice

#ifndef NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__STRUCT_H_
#define NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/PixyVector in the package nxp_cup_interfaces.
typedef struct nxp_cup_interfaces__msg__PixyVector
{
  uint64_t timestamp;
  uint8_t m0_x0;
  uint8_t m0_y0;
  uint8_t m0_x1;
  uint8_t m0_y1;
  uint8_t m1_x0;
  uint8_t m1_y0;
  uint8_t m1_x1;
  uint8_t m1_y1;
} nxp_cup_interfaces__msg__PixyVector;

// Struct for a sequence of nxp_cup_interfaces__msg__PixyVector.
typedef struct nxp_cup_interfaces__msg__PixyVector__Sequence
{
  nxp_cup_interfaces__msg__PixyVector * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} nxp_cup_interfaces__msg__PixyVector__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__STRUCT_H_
