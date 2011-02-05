#!/bin/bash

# @package LAMP
# @description Control apache2


apache2-init_exec() {
    if ! alias_loaded -s; then
        return 2
    fi
    
    local _HOST=$(alias_get "guest.host")
    local _USERNAME=$(alias_get "guest.username")
    
    guest_eval "%sudo% /etc/init.d/apache2 ${1}"
    
    return $?
}
