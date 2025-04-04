from setuptools import setup, find_packages

setup(
    name="AH_toolkit",
    version="0.1",
    packages=find_packages(),
    
    # Include AH_toolkit package
    package_dir={'': '.'},
    
    # Entry points
    entry_points={
        'console_scripts': [
            'extract_frames=src.extract_frames_from_video:main',
        ],
    },
    
    # Optional metadata
    author="Your Name",
    description="Your project description",
)