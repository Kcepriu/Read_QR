import tempfile
import os

temp_dir = tempfile.mkdtemp(prefix='some-prefix_')
temp_name = next(tempfile._get_candidate_names())


print(temp_dir)
print(temp_name)
print(os.path.join(temp_dir, temp_name)   )