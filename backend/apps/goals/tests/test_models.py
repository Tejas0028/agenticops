# from django.contrib.auth import get_user_model
# from django.test import TestCase

# from apps.departments.models import Department,DepartmentMembership
# from apps.goals.models import Goal
# from apps.organizations.models import Organization,Membership

# User = get_user_model()


# class GoalModelTest(TestCase):
#     def test_goal_creation(self):
#         org = Organization.objects.create(
#             name = "Test Org",
#             slug = "test-org",
#         )

#         department = Department.objects.create(
#             organization=org,
#             name="Engineering",
#         )

#         user = User.objects.create_user(
#             username="john",
#             password="password123",
#         )

#         membership = Membership.objects.create(
#             user=user,
#             organization=org,
#         )

#         department_membership = DepartmentMembership.objects.create(
#             department=department,
#             organization_membership=membership
#         )

#         goal = Goal.objects.create(
#             organization=org,
#             department=department,
#             owner=department_membership,
#             title="Build AI Agent",
#         )

#         self.assertEqual(
#             goal.title,
#             "Build AI Agent",
#         )