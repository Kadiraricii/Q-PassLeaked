# Professional Coding Tips - English

## What is the usage of `nmap.xml`?
Now you can ask what’s the usage of `nmap.xml`. When you want AI to implement something with that class/module, you need to give them the CODE of the class or documentation. Most AI models can read XML documentations very well and accurately.

## Why should I store the repo when reaching stable code?
TRY to store the repo when you are coming to a stable code. Why? Because we can spoil the code and not be able to run or fix it due to too many wrong fixes, one after another. So, at each stable point, commit a restore point to be able to roll back if you killed your project with wrong codes.

## Why should I test on each development/debug/fix/improvement step?
After 1 hour of development, I’m running it and getting errors one after another. That’s why I told you to test on each development/debug/fix/improvement step. I will record a video later to talk about UNIT_TESTs and logic tests and flow tests. In coding, it has techniques, but I will record how to do it in the fastest way with AI testing all possible routes.

## Why did I add `.gitkeep` to a directory after creating it before committing to git?
Because git normally doesn’t push empty directories to the repository on commit and push. So if we need that directory in our project and it’s not temporary, we need to add a file to it. Adding `.gitkeep` is a standard I normally use to force git to push the new directory to the repository on commit and push. After I add files to it, I remove the `.gitkeep`.