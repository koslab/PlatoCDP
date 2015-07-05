#!/usr/bin/env python

from genshi.template import NewTextTemplate as TextTemplate
import os

template = u'''global
        maxconn  ${maxconn}
        user haproxy
        group haproxy

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        retries 3
        option  redispatch
        timeout connect 30s
        timeout client 50s
        timeout server 50s

frontend http
    bind 0.0.0.0:80
    default_backend platocdp

backend platocdp
        option httpchk
        option forwardfor
        balance leastconn
        stats enable
        stats uri /haproxy-status
        stats refresh 5s
        cookie serverid insert indirect nocache
{% for ins in instances %}\
        server ${ins['name']} ${ins['host']}:${ins['port']} check inter 10s fastinter 1s fall 2 maxconn ${ins['threads']} slowstart 120000 on-error mark-down error-limit 5
{% end %}
'''

a = '''

'''

def main():
    tmpl = TextTemplate(template)
    instancecount = int(os.environ.get('PLATOCDP_INSTANCE_COUNT', 1))
    print tmpl.generate(**{
        'maxconn': 1024,
        'instances': [{
            'name': 'instance%s' % i,
            'host': 'instance%s.local' % i,
            'port': 8080,
            'threads': 4
        } for i in range(instancecount)]
    })

if __name__ == '__main__':
    main()
