# ci-testing

Assumed workflow:

```
feature2 ------\
                \
feature ----\    \
             \    \
develop ------*----*---\----
                        \
master ------------------*---
```


When pull request accepted into develop, a new develop release is made and uploaded.

When pull request accepted into master, a new release is made and uploaded.


anything going into develop branch is used to compile the changelog on the master branch

thus all feature branches should be squashed before going into develop.
