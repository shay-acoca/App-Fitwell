from django.core.management.base import BaseCommand

from api.models import Article, Exercise, Product, Recipe


def unsplash(photo_id, width=1000):
    return f"https://images.unsplash.com/photo-{photo_id}?w={width}&q=80&auto=format&fit=crop"


EXERCISES = {
    "Push-ups": ("1598971457999-ca4ef48a9a71", ["triceps", "shoulders", "core"], "Start in a high plank with hands under your shoulders.\nKeep your body in one straight line and lower your chest toward the floor.\nPress through your palms until your arms are straight.\nKeep your core tight for the full set."),
    "Bench Press": ("1690731033723-ad718c6e585a", ["triceps", "shoulders"], "Lie on the bench with your feet flat and shoulder blades pulled together.\nGrip the bar slightly wider than shoulder width.\nLower it to mid-chest with control.\nPress back up without bouncing the bar."),
    "Dumbbell Fly": ("1692372372344-41aed374b848", ["shoulders", "biceps"], "Lie on a bench holding dumbbells above your chest.\nKeep a slight bend in your elbows.\nOpen your arms until you feel a stretch in your chest.\nBring the dumbbells back together along the same arc."),
    "Pull-ups": ("1604233098531-90b71b1b17a6", ["biceps", "forearms", "core"], "Hang from the bar with hands slightly wider than your shoulders.\nPull your shoulder blades down and back.\nPull until your chin passes the bar.\nLower yourself slowly to a full hang."),
    "Barbell Row": ("1784819482955-e6a9523fe80d", ["biceps", "lower back"], "Hinge at the hips with a flat back and the bar below your shoulders.\nPull the bar toward your lower ribs.\nSqueeze your shoulder blades at the top.\nLower the bar with control."),
    "Lat Pulldown": ("1790094180990-02826069d59b", ["biceps", "forearms"], "Sit with your thighs secured under the pad.\nGrip the bar wider than your shoulders.\nPull it down to your upper chest while keeping your torso steady.\nLet the bar rise slowly until your arms are straight."),
    "Squats": ("1574680178050-55c6a6a96e0a", ["glutes", "hamstrings", "core"], "Stand with feet about shoulder width apart.\nBrace your core and push your hips back.\nBend your knees until your thighs are near parallel to the floor.\nDrive through your feet to stand up."),
    "Lunges": ("1784819482930-07768d5db6f6", ["glutes", "hamstrings"], "Stand tall and take a long step forward.\nLower until both knees are bent at about 90 degrees.\nKeep your front knee in line with your foot.\nPush through the front foot to return, then switch legs."),
    "Leg Press": ("1744551612249-655d096b9f95", ["glutes", "hamstrings"], "Sit with your back flat against the pad and feet shoulder width on the platform.\nRelease the safety handles.\nLower the platform until your knees reach about 90 degrees.\nPress back up without locking your knees."),
    "Military Press": ("1772450014702-498a8a3f61ae", ["triceps", "core"], "Stand with the bar resting at shoulder height.\nBrace your core and squeeze your glutes.\nPress the bar straight overhead.\nLower it back to your shoulders with control."),
    "Lateral Raises": ("1552579925-35cfbe11e850", ["trapezius"], "Stand holding dumbbells at your sides.\nKeep a slight bend in your elbows.\nRaise your arms out to shoulder height.\nLower them slowly without swinging."),
    "Arnold Press": ("1704223523449-ca3925f89dcc", ["triceps", "trapezius"], "Sit with dumbbells at shoulder height and palms facing you.\nRotate your palms forward as you press up.\nFinish with your arms extended overhead.\nReverse the rotation on the way down."),
    "Barbell Bicep Curls": ("1546483875-ad9014c88eba", ["forearms"], "Stand tall holding the bar with an underhand grip.\nKeep your elbows close to your sides.\nCurl the bar toward your shoulders.\nLower it slowly without leaning back."),
    "Tricep Dips": ("1530822847156-5df684ec5ee1", ["chest", "shoulders"], "Support yourself on parallel bars with straight arms.\nLower your body by bending your elbows.\nStop when your upper arms are about parallel to the floor.\nPress back up to the start."),
    "Plank": ("1767611116147-592ffdb14e80", ["shoulders", "glutes"], "Rest on your forearms and toes.\nKeep your body in one straight line.\nBrace your core and squeeze your glutes.\nBreathe steadily and hold for the target time."),
    "Crunch": ("1758875569284-c57e79ef75e0", ["hip flexors"], "Lie on your back with knees bent and feet flat.\nPlace your hands lightly behind your head.\nLift your shoulder blades by contracting your abs.\nLower slowly without pulling on your neck."),
    "Burpees": ("1764426445448-95103b0024a6", ["chest", "legs", "core"], "Start standing, then squat and place your hands on the floor.\nJump your feet back into a plank.\nPerform one push-up.\nJump your feet forward and finish with a vertical jump."),
    "Jump Rope": ("1514994667787-b48ca37155f0", ["calves", "shoulders"], "Hold the handles with your elbows close to your body.\nTurn the rope with your wrists.\nJump just high enough to clear the rope.\nLand softly on the balls of your feet."),
    "Thruster": ("1758875568628-12fc3376f433", ["shoulders", "glutes", "core"], "Hold the bar at shoulder height.\nPerform a full front squat.\nDrive up explosively from the bottom.\nUse that momentum to press the bar overhead."),
    "Farmer's Walk": ("1581009146145-b5ef050c2e1e", ["forearms", "trapezius", "core"], "Pick up a heavy weight in each hand.\nStand tall with your shoulders back.\nWalk with short, controlled steps.\nPut the weights down with a flat back."),
}

RECIPES = {
    "Protein Oatmeal Bowl": "1654923064926-be7e64267a31",
    "Spinach Protein Omelette": "1677844592730-ce9c936d8f1a",
    "Greek Yogurt Granola Fruit": "1641494587136-eec74f1944ae",
    "Roasted Chicken Sweet Potato": "1606791422814-b32c705e3e2f",
    "Quinoa Chicken Buddha Bowl": "1623428187969-5da2dcea5ebf",
    "Tuna Avocado Wrap": "1752095809096-f09d22c466c5",
    "Grilled Salmon Asparagus": "1748712831461-9fbf45338e13",
    "Steak Green Beans": "1778784153322-9b20b164012c",
    "Date Almond Energy Balls": "1762380832541-ddc6eb529345",
    "Post-Workout Recovery Shake": "1595348020949-87cdfbb44174",
}

PRODUCTS = {
    "Whey Protein Isolate 1kg": "1693996045300-521e9d08cabc",
    "Resistance Band Kit": "1584735935682-2f2b69dff9d2",
    "Wall Pull-Up Bar": "1772450014504-1914f8afe985",
    "Versatile Sports Mat": "1641913640860-ab4c2bfb2bb0",
    "Premium Yoga Mat": "1763004871583-4183d64096b1",
    "Compact Elliptical Bike": "1786104135351-b183105df761",
    "Weightlifting Bar 150cm": "1620188526357-ff08e03da266",
    "Adjustable Dumbbells 20kg": "1703668984128-b506579acdd2",
}

ARTICLES = {
    "The 5 Pillars of Muscle Hypertrophy": "1534438327276-14e5300c3a48",
    "Sleep: The Secret Weapon of Elite Athletes": "1545205597-3d9d02c29597",
    "Pre-Workout Nutrition: The Perfect Timing": "1546069901-ba9599a7e63c",
}


RECIPE_STEPS = {
    "Protein Oatmeal Bowl": "1. Warm the almond milk in a small pot over medium heat.\n2. Stir in the oats and cook for 2 minutes, until creamy.\n3. Take the pot off the heat, let it cool for a minute, then stir in the whey.\n4. Top with sliced banana and the peanut butter.",
    "Spinach Protein Omelette": "1. Beat the eggs in a bowl with a pinch of salt.\n2. Heat the olive oil in a non-stick pan and wilt the spinach for 1 minute.\n3. Pour in the eggs and cook over medium heat until almost set.\n4. Sprinkle with feta, fold the omelette in half and serve.",
    "Greek Yogurt Granola Fruit": "1. Spoon the Greek yogurt into a bowl.\n2. Add the granola just before eating so it stays crunchy.\n3. Top with the berries.\n4. Finish with a drizzle of honey.",
    "Roasted Chicken Sweet Potato": "1. Preheat the oven to 200\u00b0C.\n2. Cut the sweet potato and chicken into even pieces and split the broccoli into florets.\n3. Toss everything with the olive oil and paprika on a baking tray.\n4. Bake for 25 to 30 minutes, until the chicken is cooked through and the potato is tender.",
    "Quinoa Chicken Buddha Bowl": "1. Rinse the quinoa and simmer it for about 15 minutes, then fluff with a fork.\n2. Roast the chicken and chickpeas at 200\u00b0C for 20 minutes.\n3. Arrange the quinoa, chicken, chickpeas and sliced avocado in a bowl.\n4. Loosen the tahini with a little water and pour it over the bowl.",
    "Tuna Avocado Wrap": "1. Drain the tuna and flake it with a fork.\n2. Mash the avocado and spread it over the tortilla.\n3. Add the tuna, lettuce and sliced tomato.\n4. Fold in the sides and roll the wrap tightly.",
    "Grilled Salmon Asparagus": "1. Steam the asparagus for about 8 minutes, until tender.\n2. Sear the salmon skin-side down for 6 minutes in a hot pan.\n3. Flip it and cook for 2 more minutes.\n4. Finish with lemon juice, dill and the almonds.",
    "Steak Green Beans": "1. Steam the green beans for 6 to 8 minutes.\n2. Sear the steak for about 3 minutes per side, then let it rest for 5 minutes.\n3. Melt the butter in the same pan and saut\u00e9 the beans for 2 minutes.\n4. Add the garlic and thyme, cook for 1 more minute and serve with the sliced steak.",
    "Date Almond Energy Balls": "1. Blend the pitted dates, almonds, honey and half of the cacao into a sticky paste.\n2. Roll the paste into small balls.\n3. Coat the balls in the remaining cacao.\n4. Refrigerate for 30 minutes before eating.",
    "Post-Workout Recovery Shake": "1. Put the whey, frozen banana, water and creatine in a blender.\n2. Blend for 30 to 45 seconds, until smooth.\n3. Pour into a glass.\n4. Drink soon after your training session.",
}

ARTICLE_BODIES = {
    "The 5 Pillars of Muscle Hypertrophy": """<h2>Building muscle comes down to five habits</h2>
<p>Muscle growth is not the result of one secret exercise. It comes from doing a few simple things consistently, for months.</p>
<h3>1. Progressive overload</h3>
<p>Muscles adapt to the work you give them. Add a repetition, a little weight or a better range of motion over time, and record your sessions so you know whether you are actually progressing.</p>
<h3>2. Enough training volume</h3>
<p>Each muscle group needs regular hard sets during the week. Beginners can grow on a modest amount, and it makes sense to add volume only when recovery stays good.</p>
<h3>3. Clean technique and effort</h3>
<p>A controlled repetition through a full range of motion trains the target muscle better than a heavy, rushed one. Finish most working sets close to failure, while keeping your form.</p>
<h3>4. Protein and total food intake</h3>
<p>Muscle is built from what you eat. Spread protein across your meals and eat enough overall, especially when your goal is to gain weight.</p>
<h3>5. Recovery</h3>
<p>Growth happens between sessions. Good sleep, rest days and a manageable training load matter as much as the workout itself.</p>""",
    "Sleep: The Secret Weapon of Elite Athletes": """<h2>Why sleep belongs in your training plan</h2>
<p>Training creates the stimulus, and sleep is when much of the repair takes place. Short nights tend to make sessions feel harder and make it more difficult to stay focused.</p>
<h3>What happens at night</h3>
<p>During sleep the body restores energy and repairs tissue, and the brain consolidates what it has learned, including new movement patterns.</p>
<h3>How much do you need?</h3>
<p>Most adults do best with seven to nine hours per night. If you train hard or often, aim for the upper part of that range.</p>
<h3>Simple habits that help</h3>
<p>Go to bed and wake up at regular times, keep your room dark and cool, avoid caffeine late in the day and put screens away before bed.</p>
<h3>When to get help</h3>
<p>If you often sleep badly or feel exhausted despite long nights, talk to a doctor. This article is general information and does not replace medical advice.</p>""",
    "Pre-Workout Nutrition: The Perfect Timing": """<h2>What to eat, and when, before training</h2>
<p>The food you eat across the whole day matters more than a single meal. Still, good timing can help you feel better during a session.</p>
<h3>Two to three hours before</h3>
<p>Have a complete meal with carbohydrates, protein and a little fat, such as chicken with rice and vegetables.</p>
<h3>Thirty to sixty minutes before</h3>
<p>Choose something small and easy to digest, such as a banana or a yogurt. Large or very fatty meals close to training can cause discomfort.</p>
<h3>Hydration</h3>
<p>Drink regularly during the day and bring water to your session, especially when it is hot or you sweat a lot.</p>
<h3>After training</h3>
<p>There is no need to rush for a shake the moment you finish. Have a normal meal with protein and carbohydrates within the next few hours, and keep your daily intake on target.</p>""",
}


class Command(BaseCommand):
    help = "Applies verified images and exercise instructions to seeded content. Safe to run repeatedly."

    def handle(self, *args, **options):
        counts = {"exercises": 0, "recipes": 0, "products": 0, "articles": 0}
        for name, (photo, secondary, instructions) in EXERCISES.items():
            counts["exercises"] += Exercise.objects.filter(name=name).update(
                image_url=unsplash(photo), secondary_muscles=secondary, instructions=instructions
            )
        for title, photo in RECIPES.items():
            counts["recipes"] += Recipe.objects.filter(title=title).update(
                image_url=unsplash(photo), instructions=RECIPE_STEPS[title]
            )
        for name, photo in PRODUCTS.items():
            counts["products"] += Product.objects.filter(name=name).update(image=unsplash(photo))
        for title, photo in ARTICLES.items():
            counts["articles"] += Article.objects.filter(title=title).update(image=unsplash(photo, 1400))
        # Article text is only completed while it is still a stub, so edited articles are kept.
        for article in Article.objects.filter(title__in=ARTICLE_BODIES):
            if len(article.content.strip()) < 300:
                article.content = ARTICLE_BODIES[article.title]
                article.save(update_fields=["content"])
        self.stdout.write(self.style.SUCCESS(f"Content synchronized: {counts}"))
