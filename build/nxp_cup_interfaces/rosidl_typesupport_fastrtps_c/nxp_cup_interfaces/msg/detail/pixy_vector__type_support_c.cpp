// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice
#include "nxp_cup_interfaces/msg/detail/pixy_vector__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "nxp_cup_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "nxp_cup_interfaces/msg/detail/pixy_vector__struct.h"
#include "nxp_cup_interfaces/msg/detail/pixy_vector__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _PixyVector__ros_msg_type = nxp_cup_interfaces__msg__PixyVector;

static bool _PixyVector__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _PixyVector__ros_msg_type * ros_message = static_cast<const _PixyVector__ros_msg_type *>(untyped_ros_message);
  // Field name: timestamp
  {
    cdr << ros_message->timestamp;
  }

  // Field name: m0_x0
  {
    cdr << ros_message->m0_x0;
  }

  // Field name: m0_y0
  {
    cdr << ros_message->m0_y0;
  }

  // Field name: m0_x1
  {
    cdr << ros_message->m0_x1;
  }

  // Field name: m0_y1
  {
    cdr << ros_message->m0_y1;
  }

  // Field name: m1_x0
  {
    cdr << ros_message->m1_x0;
  }

  // Field name: m1_y0
  {
    cdr << ros_message->m1_y0;
  }

  // Field name: m1_x1
  {
    cdr << ros_message->m1_x1;
  }

  // Field name: m1_y1
  {
    cdr << ros_message->m1_y1;
  }

  return true;
}

static bool _PixyVector__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _PixyVector__ros_msg_type * ros_message = static_cast<_PixyVector__ros_msg_type *>(untyped_ros_message);
  // Field name: timestamp
  {
    cdr >> ros_message->timestamp;
  }

  // Field name: m0_x0
  {
    cdr >> ros_message->m0_x0;
  }

  // Field name: m0_y0
  {
    cdr >> ros_message->m0_y0;
  }

  // Field name: m0_x1
  {
    cdr >> ros_message->m0_x1;
  }

  // Field name: m0_y1
  {
    cdr >> ros_message->m0_y1;
  }

  // Field name: m1_x0
  {
    cdr >> ros_message->m1_x0;
  }

  // Field name: m1_y0
  {
    cdr >> ros_message->m1_y0;
  }

  // Field name: m1_x1
  {
    cdr >> ros_message->m1_x1;
  }

  // Field name: m1_y1
  {
    cdr >> ros_message->m1_y1;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_nxp_cup_interfaces
size_t get_serialized_size_nxp_cup_interfaces__msg__PixyVector(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _PixyVector__ros_msg_type * ros_message = static_cast<const _PixyVector__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name timestamp
  {
    size_t item_size = sizeof(ros_message->timestamp);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m0_x0
  {
    size_t item_size = sizeof(ros_message->m0_x0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m0_y0
  {
    size_t item_size = sizeof(ros_message->m0_y0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m0_x1
  {
    size_t item_size = sizeof(ros_message->m0_x1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m0_y1
  {
    size_t item_size = sizeof(ros_message->m0_y1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m1_x0
  {
    size_t item_size = sizeof(ros_message->m1_x0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m1_y0
  {
    size_t item_size = sizeof(ros_message->m1_y0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m1_x1
  {
    size_t item_size = sizeof(ros_message->m1_x1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name m1_y1
  {
    size_t item_size = sizeof(ros_message->m1_y1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _PixyVector__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_nxp_cup_interfaces__msg__PixyVector(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_nxp_cup_interfaces
size_t max_serialized_size_nxp_cup_interfaces__msg__PixyVector(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: timestamp
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: m0_x0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m0_y0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m0_x1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m0_y1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m1_x0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m1_y0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m1_x1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: m1_y1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static size_t _PixyVector__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_nxp_cup_interfaces__msg__PixyVector(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_PixyVector = {
  "nxp_cup_interfaces::msg",
  "PixyVector",
  _PixyVector__cdr_serialize,
  _PixyVector__cdr_deserialize,
  _PixyVector__get_serialized_size,
  _PixyVector__max_serialized_size
};

static rosidl_message_type_support_t _PixyVector__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_PixyVector,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, nxp_cup_interfaces, msg, PixyVector)() {
  return &_PixyVector__type_support;
}

#if defined(__cplusplus)
}
#endif
