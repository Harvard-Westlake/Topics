# Activity - Bouncing Ball

*Concept: Draw a frame, move the ball a little, and let the browser call you again until it looks like motion.*

![Animated diagram of the animation loop. On the left, four steps in a cycle that light up in turn: 1 clear the canvas, 2 draw everything, 3 move everything a little, 4 ask for the next frame with requestAnimationFrame. On the right, a canvas where a ball slides across and bounces off the edges while a frame counter climbs. A caption explains that the browser runs the cycle about 60 times a second and your eye turns the still frames into movement.](../assets/animation-loop.svg)

## Task

1. Add `<canvas id="stage" width="400" height="300"></canvas>` to `public/index.html`, create `scripts/ball.js` with the bouncing ball code from the lesson, and link it with its own `<script defer src="scripts/ball.js"></script>` tag. Refresh: the ball bounces.
2. Change `speed` to 8, then to 1. Change the ball's `fillStyle`. Each edit, save, refresh shows a different animation from the same loop.
3. Comment out the `clearRect` line and refresh. The ball leaves a trail, because every frame now draws on top of the last one. Put the line back.
4. Add a `keydown` listener: `ArrowUp` makes `speed` 1.5 times bigger and `ArrowDown` 1.5 times smaller. The next frame uses the new value. An event changing what the loop draws is the whole idea of a game.
5. In your terminal, run `firebase deploy --only hosting` and open your live address. The ball bounces for anyone, on any device.
