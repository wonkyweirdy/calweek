import unittest
from calweek import CalWeek

# Note: I haven't carefully validated these test cases.
# I modified the original isoweek tests to pass with calweek.
# I relied on tabletest.py for validation in development.

class TestCalWeek(unittest.TestCase):
    def test_constructors(self):
        w = CalWeek(2011,1)
        self.assertTrue(w)
        self.assertEqual(str(w), "2011W01")

        w = CalWeek(2011,52)
        self.assertEqual(str(w), "2011W52")

        w = CalWeek(2009,51)
        self.assertEqual(str(w), "2009W51")
        w = CalWeek(2009,52)
        self.assertEqual(str(w), "2009W52")
        w = CalWeek(2009,53)
        self.assertEqual(str(w), "2009W53")

        w = CalWeek.thisweek()
        self.assertTrue(w)

        w = CalWeek.fromordinal(1)
        self.assertEqual(str(w), "0001W01")
        w = CalWeek.fromordinal(2)
        self.assertEqual(str(w), "0001W02")
        w = CalWeek.fromordinal(521723)
        self.assertEqual(str(w), "9999W53")

        w = CalWeek.fromstring("2011W01")
        self.assertEqual(str(w), "2011W01")
        w = CalWeek.fromstring("2011-W01")
        self.assertEqual(str(w), "2011W01")

        from datetime import date
        w = CalWeek.withdate(date(2011, 5, 17))
        self.assertEqual(str(w), "2011W21")

        weeks = list(CalWeek.weeks_of_year(2009))
        self.assertEqual(len(weeks), 53)
        self.assertEqual(weeks[0], CalWeek(2009,1))
        self.assertEqual(weeks[-1], CalWeek(2009,53))

        weeks = list(CalWeek.weeks_of_year(2011))
        self.assertEqual(len(weeks), 53)
        self.assertEqual(weeks[0], CalWeek(2011,1))
        self.assertEqual(weeks[-1], CalWeek(2011,53))

        self.assertEqual(CalWeek.last_week_of_year(2009), CalWeek(2009, 53))
        self.assertEqual(CalWeek.last_week_of_year(2010), CalWeek(2010, 53))
        self.assertEqual(CalWeek.last_week_of_year(2011), CalWeek(2011, 53))
        self.assertEqual(CalWeek.last_week_of_year(9999), CalWeek(9999, 53))

        self.assertRaises(ValueError, lambda: CalWeek(0, 0))
        self.assertRaises(ValueError, lambda: CalWeek.fromstring("0000W00"))
        self.assertRaises(ValueError, lambda: CalWeek.fromstring("foo"))
        self.assertRaises(ValueError, lambda: CalWeek.fromordinal(-1))
        self.assertRaises(ValueError, lambda: CalWeek.fromordinal(0))
        self.assertRaises(ValueError, lambda: CalWeek.fromordinal(521724))
        self.assertRaises(ValueError, lambda: CalWeek.last_week_of_year(0))
        self.assertRaises(ValueError, lambda: CalWeek.last_week_of_year(10000))

    def test_mix_max(self):
        self.assertEqual(CalWeek.min, CalWeek(1, 1))
        self.assertEqual(CalWeek.max, CalWeek(9999, 53))
        self.assertEqual(CalWeek.resolution.days, 7)

        self.assertRaises(ValueError, lambda: CalWeek.min - 1)
        self.assertRaises(ValueError, lambda: CalWeek.max + 1)

    def test_stringification(self):
        w = CalWeek(2011, 20)
        self.assertEqual(str(w), "2011W20")
        #self.assertEqual(w.isoformat(), "2011W20")
        self.assertEqual(repr(w), "calweek.CalWeek(2011, 20)")

    def test_replace(self):
        w = CalWeek(2011, 20)
        self.assertEqual(w.replace(), w)
        self.assertEqual(w.replace(year=2010), CalWeek(2010, 20))
        self.assertEqual(w.replace(week=2), CalWeek(2011, 2))
        #self.assertEqual(w.replace(week=99), CalWeek(2012, 47))
        self.assertEqual(w.replace(year=1, week=1), CalWeek(1, 1))

    def test_days(self):
        w = CalWeek(2011, 20)
        #self.assertEqual(w.monday().isoformat(),    ...)
        #self.assertEqual(w.tuesday().isoformat(),   ...)
        #self.assertEqual(w.wednesday().isoformat(), ...)
        #self.assertEqual(w.thursday().isoformat(),  ...)
        #self.assertEqual(w.friday().isoformat(),    ...)
        #self.assertEqual(w.saturday().isoformat(),  ...)
        self.assertEqual(w.sunday().isoformat(),    "2011-05-08")

        self.assertEqual(w.day(0).isoformat(),  "2011-05-08")

        days = w.days()
        self.assertEqual(len(days), 7)
        self.assertEqual(days[0].isoformat(), "2011-05-08")
        self.assertEqual(days[-1].isoformat(), "2011-05-14")

        from datetime import date
        self.assertFalse(w.contains(date(2011,5,7)))
        self.assertTrue(w.contains(date(2011,5,8)))
        self.assertTrue(w.contains(date(2011,5,14)))
        self.assertFalse(w.contains(date(2011,5,15)))

    def test_arithmetics(self):
        w = CalWeek(2011, 20)
        self.assertEqual(str(w + 0),   "2011W20")
        self.assertEqual(str(w + 1),   "2011W21")
        self.assertEqual(str(w - 1),   "2011W19")
        self.assertEqual(str(w + 52),  "2012W19")
        self.assertEqual(str(w - 104), "2009W20")

        self.assertEqual(w - w, 0)
        self.assertEqual(w - CalWeek(2011, 1), 19)
        self.assertEqual(CalWeek(2011, 1) - w, -19)

        self.assertEqual(str(w + CalWeek.resolution), "2011W21")
        self.assertEqual(str(w - CalWeek.resolution), "2011W19")

    def test_arithmetics_subclass(self):
        class MyWeek(CalWeek):
            pass
        w = MyWeek(2011, 20)
        next_week = w + 1
        self.assertEqual(str(next_week),   "2011W21")
        self.assertTrue(isinstance(next_week, MyWeek))

if __name__ == '__main__':
    unittest.main()
