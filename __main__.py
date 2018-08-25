#!/usr/bin/env python
import optparse


def main():
    p = optparse.OptionParser()
    p.add_option('--person', '-p', default="world")  # sample arg handling
    options, arguments = p.parse_args()
    print('Hello %s' % options.person)  # sample arg handling


if __name__ == '__main__':
    main()
