import { Alarm } from '@mui/icons-material';
import { AppBar, IconButton, Toolbar, Typography } from '@mui/material';
import Button from "@mui/material/Button";
import type { NextPage } from 'next';
import { useRecoilState } from "recoil";
import { countInfo } from "../reducers/stores";

const Home: NextPage = () => {
  const [count, setCount] = useRecoilState(countInfo);
  return (
    <div>
      <AppBar color="primary" position="static">
        <Toolbar>
          <Typography color="inherit">
            TypeScript + NextJs + MUI  START!!!
          </Typography>
        </Toolbar>
      </AppBar>
      <Button variant="contained" color="success" onClick={() => setCount(count + 1)}>material Button {count}</Button><br/>
      <IconButton color="secondary" aria-label="add an alarm">
        <Alarm />
      </IconButton>
    </div>
  );
}

export default Home