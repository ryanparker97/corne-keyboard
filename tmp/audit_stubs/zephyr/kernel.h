
#pragma once
#include <stdbool.h>
#include <stdint.h>
#define K_FOREVER 0
#define SYS_SLIST_STATIC_INIT(x) {0}
typedef struct sys_snode { struct sys_snode *next; } sys_snode_t;
typedef struct { sys_snode_t *head; } sys_slist_t;
static inline void sys_slist_append(sys_slist_t *l, sys_snode_t *n) {}
#define SYS_SLIST_FOR_EACH_CONTAINER(list, var, member) for ((var)=0; (var)!=0; )
#define IS_ENABLED(x) x
