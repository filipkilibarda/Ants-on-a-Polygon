Ants on a Polygon...
----
So you have `n` ants arranged on a symetrical polygon with `n` sides. Each ant moves toward the ant infront of it. We can assume that each ant starts a distance, `1` from the ant infront of it and moves at a speed `1`.

Question
----
How long does it take for them to reach the center?

Solution
----
Thanks to [Jake Vanderplas' animation tutorial](https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/), I was able to make a cool animation out of this problem.

So start off with just 4 ants, because that's the simplest case, and you'll see why.

![ants on a polygon](/out.gif?raw=true)

Since each ant is moving at the same speed, and each ant starts the same distance from the ant in front of it, the problem remains completely symetrical through time. Thus, in the case of 4 ants arranged on a square, we can assume that they will continue to form a perfect square untill they all reach the middle.

Now that we've established that understanding, we can ask, how fast is each ant closing in on the ant in front of it. Looking at the figure below, the angle formed between `ant1` and `ant2` is `90 degrees`. So `ant2` is always moving exactly *perpendicular* to `ant1`, which means that `ant2` is never moving *away* from `ant1`. Thus, we can conclude that `ant1` is closing in on `ant2` at a speed of `v`.

![just a few ants arranged on a square](/square.png?raw=true)

Produced with ![GeoGebra](https://www.math10.com/en/geometry/geogebra/geogebra.html).
