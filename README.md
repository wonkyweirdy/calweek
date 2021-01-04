CalWeek class
=============

The calweek module provide the class *CalWeek*.  Instances represent
specific weeks spanning 7 days Sunday to Saturday except weeks at the year
beginning/end may be shorter.  There are 53 or 54 numbered weeks in a year.
Week 1 is always starts on January 1 of the year.

This is a traditional week number system different from the
[ISO 8601]( https://en.wikipedia.org/wiki/ISO_8601) standard.
ISO 8601 week numbering is now more predominate, but still sometimes
software needs to work with the old system.

For ISO 8601 week support in Python, use the
[isoweek](https://pypi.org/project/isoweek/)
module on which this code was based.

The *CalWeek* instances are light weight and immutable with an interface similar
to the datetime.date objects.  Example code:

    from calweek import CalWeek
    w = CalWeek(2011, 20)
    print "Week %s starts on %s" % (w, w.day(0))

    print "Current week number is", CalWeek.thisweek().week
    print "Next week is", CalWeek.thisweek() + 1

weeknum() function
==================

The calweek module also includes a *weeknum()* function compatible with
Microsoft Excel's WEEKNUM formula function.
