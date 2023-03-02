// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice

#ifndef NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__FUNCTIONS_H_
#define NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "nxp_cup_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "nxp_cup_interfaces/msg/detail/pixy_vector__struct.h"

/// Initialize msg/PixyVector message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * nxp_cup_interfaces__msg__PixyVector
 * )) before or use
 * nxp_cup_interfaces__msg__PixyVector__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
bool
nxp_cup_interfaces__msg__PixyVector__init(nxp_cup_interfaces__msg__PixyVector * msg);

/// Finalize msg/PixyVector message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
void
nxp_cup_interfaces__msg__PixyVector__fini(nxp_cup_interfaces__msg__PixyVector * msg);

/// Create msg/PixyVector message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * nxp_cup_interfaces__msg__PixyVector__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
nxp_cup_interfaces__msg__PixyVector *
nxp_cup_interfaces__msg__PixyVector__create();

/// Destroy msg/PixyVector message.
/**
 * It calls
 * nxp_cup_interfaces__msg__PixyVector__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
void
nxp_cup_interfaces__msg__PixyVector__destroy(nxp_cup_interfaces__msg__PixyVector * msg);


/// Initialize array of msg/PixyVector messages.
/**
 * It allocates the memory for the number of elements and calls
 * nxp_cup_interfaces__msg__PixyVector__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
bool
nxp_cup_interfaces__msg__PixyVector__Sequence__init(nxp_cup_interfaces__msg__PixyVector__Sequence * array, size_t size);

/// Finalize array of msg/PixyVector messages.
/**
 * It calls
 * nxp_cup_interfaces__msg__PixyVector__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
void
nxp_cup_interfaces__msg__PixyVector__Sequence__fini(nxp_cup_interfaces__msg__PixyVector__Sequence * array);

/// Create array of msg/PixyVector messages.
/**
 * It allocates the memory for the array and calls
 * nxp_cup_interfaces__msg__PixyVector__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
nxp_cup_interfaces__msg__PixyVector__Sequence *
nxp_cup_interfaces__msg__PixyVector__Sequence__create(size_t size);

/// Destroy array of msg/PixyVector messages.
/**
 * It calls
 * nxp_cup_interfaces__msg__PixyVector__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_nxp_cup_interfaces
void
nxp_cup_interfaces__msg__PixyVector__Sequence__destroy(nxp_cup_interfaces__msg__PixyVector__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__FUNCTIONS_H_
