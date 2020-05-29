I'm concerned with how arcane this feels. Like, "I don't know why it works, but it does. I think."
Why does the mocked method under test return a mock object instead of the expected value/side effect?
Is @patch actually passing a patched object in as mock_process ? If so, why doesn't it work when I glue a mocked method to that variable?

I'm inclined to simplify all of these, and use create=True  to clean up the macOS issues, but this language makes me a bit nervous: 
It is off by default because it can be dangerous. With it switched on you can write passing tests against APIs that don’t actually exist!

This works:
```
    @mock.patch("q2_diversity_lib._util.psutil.Process")
    def test_function_with_an_n_jobs_param(self, mock_process):
        mock_process = psutil.Process()
        mock_process.cpu_affinity = mock.MagicMock(return_value=[0, 1, 2])
        self.assertEqual(self.function_w_n_jobs_param(3), 3)
```

-----------------------------------------------------------------------------

This fails with "ValueError: The value of n_jobs cannot exceed the number of processors (0) available in this system."
```
    @mock.patch("q2_diversity_lib._util.psutil.Process")
    def test_function_with_an_n_jobs_param(self, mock_process):
        # Unlesss we manually set mock_process to the mocked `psutil.Process`,
        # calls to psutil.Process.cpu_affinity return an object
        # mock_process = psutil.Process()
        mock_process.cpu_affinity = mock.MagicMock(return_value=[0, 1, 2])
        self.assertEqual(self.function_w_n_jobs_param(3), 3)
```
Interestingly, this line 
`print(psutil.Process().cpu_affinity())`

in the code under test yields an object <MagicMock name='Process().cpu_affinity()' id='139830060822312'>, not the return value of psutil.Process().cpu_affinity()


-----------------------------------------------------------------------------

This also works. It doesn't seem to matter what variable we assign our passed mock to: 
```
    @mock.patch("q2_diversity_lib._util.psutil.Process")
    def test_function_with_an_n_jobs_param(self, mock_cpu_affinity):
        thing = psutil.Process()
        thing.cpu_affinity = mock.MagicMock(return_value=[0, 1, 2])
        self.assertEqual(self.function_w_n_jobs_param(3), 3)
```

-----------------------------------------------------------------------------

This works (Linux - likely subject to create=true issues on mac):
```
    @mock.patch("q2_diversity_lib._util.psutil.Process.cpu_affinity",
                return_value=[0, 1, 2])
    def test_function_with_an_n_jobs_param(self, mock_process):
        self.assertEqual(self.function_w_n_jobs_param(3), 3)
```

