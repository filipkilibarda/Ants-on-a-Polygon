Ants on a Polygon...
----
So you have `n` ants arranged on the verticies of a symetrical polygon with `n` sides. Each ant moves exactly toward the ant infront of it until they all reach the center. We can assume that each ant starts a distance, `d` from the ant infront of it and moves at a speed `v`.

![ants on a polygon](/imgs/ants8.gif?raw=true)

Question
----
How long does it take for them to reach the center?

Solution
----
Thanks to [Jake Vanderplas' animation tutorial](https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/), I was able to make a cool animation out of this problem.

So start off with just 4 ants, because that's the simplest case, and you'll see why.

![ants on a polygon](/imgs/ants4.gif?raw=true)

Since each ant is moving at the same speed, and each ant starts the same distance from the ant in front of it, the problem remains completely symetrical through time. Thus, in the case of 4 ants arranged on a square, we can assume that they will continue to form a perfect square untill they all reach the middle.

Instead of asking how long before they reach the middle, ask how long before one ant catches up to the ant infront of it? 

Since the ant infront is always moving perpendicular to the ant that's following, we can conclude that the speed at which the follower is closing in on the ant infront is `v`, the speed of the ant itself. Which means, it will take `d/v` for each ant to catch up to the ant infront.

![just a few ants arranged on a square](/imgs/square.png?raw=true)

Produced with [GeoGebra](https://www.math10.com/en/geometry/geogebra/geogebra.html).

How about with `n` ants arranged on a polygon with `n` sides?

![general case](/imgs/general.png?raw=true)

The problem can still be approached in the same way. How fast is the follower closing in on the ant infront?

First we need to find how fast the ant infront is moving relative to the follower. Using the interior angle formula 

    (n-2) × 180° / n
    
where `n` is the number of sides, we can determine the angle `a` as shown in the image. From that, we determine that the ant infront is moving at a speed of 

    v sin(a)

relative to the ant behind. Taking the difference of the two speeds we get

    v - v sin(a)
    
as the speed at which the ants are closing in on each other. Now all we have to do is divide the initial separation, `d`, by the speed that the ants are closing in on each other.

    t = d/v/(1-sin(a))

Gives us the time it takes for the ants to reach the center.
