defmodule K3p7wqTest do
  use ExUnit.Case
  doctest K3p7wq

  test "greets the world" do
    assert K3p7wq.hello() == :world
  end

  # Poängen med hela spåret: supervisorn reser upp processer (q4m8t2.md,
  # "Arise"). Testerna nedan kör på host — samma OTP-modell som i firmwaren.

  test "supervisor-trädet är uppe" do
    assert is_pid(Process.whereis(K3p7wq.Supervisor))
  end

  test "applikationen är startad" do
    assert List.keyfind(Application.started_applications(), :k3p7wq, 0)
  end

  test "supervisorn svarar på count_children" do
    assert %{specs: _, active: _, supervisors: _, workers: _} =
             Supervisor.count_children(K3p7wq.Supervisor)
  end

  test "supervisorn reser upp en dödad process" do
    spec = %{
      id: :arise,
      start: {Agent, :start_link, [fn -> :alive end, [name: :arise]]}
    }

    {:ok, first} = Supervisor.start_child(K3p7wq.Supervisor, spec)
    ref = Process.monitor(first)
    Process.exit(first, :kill)
    assert_receive {:DOWN, ^ref, :process, ^first, :killed}, 1_000

    second = wait_for_restart(:arise, first)
    assert is_pid(second)
    assert second != first
    assert Agent.get(second, & &1) == :alive

    :ok = Supervisor.terminate_child(K3p7wq.Supervisor, :arise)
    :ok = Supervisor.delete_child(K3p7wq.Supervisor, :arise)
  end

  defp wait_for_restart(name, old_pid, tries \\ 50) do
    case Process.whereis(name) do
      pid when is_pid(pid) and pid != old_pid ->
        pid

      _ when tries > 0 ->
        Process.sleep(10)
        wait_for_restart(name, old_pid, tries - 1)

      _ ->
        flunk("#{inspect(name)} restartades aldrig")
    end
  end
end
