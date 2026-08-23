# Activity — The Locker Problem

*Concept: The birthday paradox makes collisions far more likely than intuition suggests, and the collision formula tells you exactly how much space "safe" costs.*

![Chart of collision probability versus the number of people in the room, for 365 possible birthdays. The curve races upward: at just 23 people the probability of a shared birthday already reaches 50%, and by 60 people it exceeds 99%. What matters is pairs, not people — k people form k(k−1)/2 chances to collide.](../assets/the-locker-problem.svg)

## Task

1. On paper or with a calculator, use the collision formula $P = 1 - e^{-\frac{k(k-1)}{2N}}$ with your actual class. Set $k$ to the number of students in the room and $N = 365$ (days of the year). Compute the probability that two people in the room share a birthday. (For $k = 24$: $P = 1 - e^{-\frac{24 \cdot 23}{730}} \approx 0.53$ — better than a coin flip.)
2. Check the prediction against reality: go around the room and see if two people actually share a birthday.
3. Now flip the formula around. Using $N \geq \frac{-k(k-1)}{2\ln(P)}$, calculate how many lockers your class would need so there is **less than a 1% chance** any two students are randomly assigned the same locker ($P = 0.99$).
4. Write one sentence answering: why does the required $N$ grow so much faster than $k$? (The chart's caption has the key idea.)
